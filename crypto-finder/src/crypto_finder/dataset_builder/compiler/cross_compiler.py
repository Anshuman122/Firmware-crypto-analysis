"""
Cross-architecture compilation system

Compiles crypto libraries for multiple target architectures:
- x86, x86-64, ARM, AArch64, MIPS, RISC-V
- Multiple optimization levels (-O0, -O1, -O2, -O3, -Os)
- Multiple compilers (GCC, Clang)
"""

import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
import json
from tqdm import tqdm

from crypto_finder.common.logging import setup_logging
from crypto_finder.common.exceptions import CompilationError
from .library_manager import LibraryManager

logger = setup_logging(__name__)


class CrossCompiler:
    """
    Manages cross-compilation of crypto libraries
    """
    
    # Architecture configurations
    ARCHITECTURES = {
        'x86': {
            'cc': 'gcc',
            'cflags': '-m32',
            'triplet': 'i686-linux-gnu',
            'description': 'Intel x86 32-bit'
        },
        'x86-64': {
            'cc': 'gcc',
            'cflags': '-m64',
            'triplet': 'x86_64-linux-gnu',
            'description': 'Intel x86 64-bit'
        },
        'arm': {
            'cc': 'arm-linux-gnueabi-gcc',
            'cflags': '',
            'triplet': 'arm-linux-gnueabi',
            'description': 'ARM 32-bit'
        },
        'aarch64': {
            'cc': 'aarch64-linux-gnu-gcc',
            'cflags': '',
            'triplet': 'aarch64-linux-gnu',
            'description': 'ARM 64-bit (AArch64)'
        },
        'mips': {
            'cc': 'mips-linux-gnu-gcc',
            'cflags': '',
            'triplet': 'mips-linux-gnu',
            'description': 'MIPS 32-bit'
        },
        'riscv': {
            'cc': 'riscv64-linux-gnu-gcc',
            'cflags': '',
            'triplet': 'riscv64-linux-gnu',
            'description': 'RISC-V 64-bit'
        }
    }
    
    # Optimization levels to test
    OPTIMIZATION_LEVELS = ['-O0', '-O1', '-O2', '-O3', '-Os']
    
    # Compilers to use
    COMPILERS = ['gcc', 'clang']
    
    def __init__(self, workspace_dir: str = "workspace"):
        """
        Initialize cross-compiler
        
        Args:
            workspace_dir: Working directory for compilation
        """
        self.workspace = Path(workspace_dir)
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # Check available toolchains
        self.available_archs = self._check_toolchains()
        logger.info(f"Available architectures: {', '.join(self.available_archs)}")
    
    def _check_toolchains(self) -> List[str]:
        """
        Check which cross-compilation toolchains are installed
        
        Returns:
            List of available architecture names
        """
        available = []
        
        for arch, config in self.ARCHITECTURES.items():
            cc = config['cc']
            if shutil.which(cc):
                available.append(arch)
                logger.debug(f"✓ {arch}: {cc} found")
            else:
                logger.warning(f"✗ {arch}: {cc} not found - skipping")
        
        if not available:
            raise CompilationError("No cross-compilers found! Install toolchains first.")
        
        return available
    
    def compile_file(
        self,
        source_file: str,
        output_file: str,
        architecture: str,
        optimization: str = '-O2',
        compiler: str = 'gcc',
        extra_flags: Optional[List[str]] = None
    ) -> bool:
        """
        Compile a single C/C++ source file
        
        Args:
            source_file: Path to source file
            output_file: Where to save compiled binary
            architecture: Target architecture
            optimization: Optimization level
            compiler: Compiler to use (gcc or clang)
            extra_flags: Additional compiler flags
        
        Returns:
            True if compilation succeeded
        """
        if architecture not in self.available_archs:
            logger.error(f"Architecture {architecture} not available")
            return False
        
        arch_config = self.ARCHITECTURES[architecture]
        
        # Build compiler command
        cc = arch_config['cc']
        
        # For clang, modify the command
        if compiler == 'clang' and architecture in ['x86', 'x86-64']:
            cc = 'clang'
            if architecture == 'x86':
                target_flag = '--target=i686-linux-gnu'
            else:
                target_flag = '--target=x86_64-linux-gnu'
        else:
            target_flag = ''
        
        # Build flags list
        flags = [
            optimization,
            arch_config['cflags'],
            target_flag,
            '-static',  # Create standalone binary
            '-fno-stack-protector',  # Disable stack protection for analysis
            '-o', output_file,
            source_file
        ]
        
        if extra_flags:
            flags.extend(extra_flags)
        
        # Remove empty flags
        flags = [f for f in flags if f]
        
        # Compile
        cmd = [cc] + flags
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.debug(f"✓ Compiled: {output_file}")
                return True
            else:
                logger.error(f"✗ Compilation failed: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error(f"✗ Compilation timeout: {source_file}")
            return False
        except Exception as e:
            logger.error(f"✗ Compilation error: {e}")
            return False
    
    def compile_library(
        self,
        library_name: str,
        source_dir: str,
        functions: List[str],
        output_dir: str
    ) -> Dict[str, Dict]:
        """
        Compile all functions from a library for all architectures
        
        Args:
            library_name: Name of the library (e.g., 'openssl')
            source_dir: Directory containing source files
            functions: List of function names to compile
            output_dir: Where to save compiled binaries
        
        Returns:
            Dictionary mapping (arch, opt, func) to binary info
        """
        results = {}
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        total_compilations = (
            len(self.available_archs) * 
            len(self.OPTIMIZATION_LEVELS) * 
            len(functions)
        )
        
        logger.info(f"Compiling {library_name}: {total_compilations} total compilations")
        
        with tqdm(total=total_compilations, desc=f"Compiling {library_name}") as pbar:
            for arch in self.available_archs:
                for opt in self.OPTIMIZATION_LEVELS:
                    for func_name in functions:
                        # Find source file for this function
                        source_file = self._find_source_file(source_dir, func_name)
                        
                        if not source_file:
                            logger.warning(f"Source not found for {func_name}")
                            pbar.update(1)
                            continue
                        
                        # Generate output filename
                        opt_clean = opt.replace('-', '').lower()
                        output_file = (
                            output_path / 
                            f"{library_name}_{func_name}_{arch}_{opt_clean}.bin"
                        )
                        
                        # Compile
                        success = self.compile_file(
                            source_file=source_file,
                            output_file=str(output_file),
                            architecture=arch,
                            optimization=opt
                        )
                        
                        if success:
                            # Store metadata
                            key = (arch, opt, func_name)
                            results[key] = {
                                'binary_path': str(output_file),
                                'source_path': str(source_file),
                                'architecture': arch,
                                'optimization': opt,
                                'function': func_name,
                                'library': library_name,
                                'size': output_file.stat().st_size,
                                'md5': self._compute_md5(output_file)
                            }
                        
                        pbar.update(1)
        
        logger.info(f"Compiled {len(results)}/{total_compilations} successfully")
        return results
    
    def _find_source_file(self, source_dir: str, function_name: str) -> Optional[str]:
        """
        Find source file containing a specific function
        
        Args:
            source_dir: Directory to search
            function_name: Function name to find
        
        Returns:
            Path to source file or None
        """
        source_path = Path(source_dir)
        
        # Common naming patterns
        patterns = [
            f"{function_name}.c",
            f"{function_name}.cpp",
            f"*{function_name}*.c",
            f"*{function_name}*.cpp"
        ]
        
        for pattern in patterns:
            matches = list(source_path.rglob(pattern))
            if matches:
                return str(matches[0])
        
        return None
    
    def _compute_md5(self, file_path: Path) -> str:
        """
        Compute MD5 hash of a file
        
        Args:
            file_path: File to hash
        
        Returns:
            MD5 hex digest
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()


class DatasetCompiler:
    """
    High-level interface for building complete datasets
    """
    
    def __init__(self, config: Dict, output_dir: str):
        """
        Initialize dataset compiler
        
        Args:
            config: Configuration dictionary
            output_dir: Where to save compiled binaries
        """
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.compiler = CrossCompiler(str(self.output_dir / 'workspace'))
        self.library_manager = LibraryManager(str(self.output_dir / 'sources'))
    
    def compile_all(self):
        """
        Compile all configured crypto libraries
        """
        libraries = self.config.get('crypto_libraries', [])
        
        logger.info(f"Starting compilation of {len(libraries)} libraries")
        
        all_results = {}
        
        for lib_config in libraries:
            lib_name = lib_config['name']
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {lib_name}")
            logger.info(f"{'='*60}")
            
            # Download library if needed
            source_dir = self.library_manager.get_library(
                lib_name,
                lib_config.get('version'),
                lib_config.get('url')
            )
            
            # Get functions to compile
            functions = self._get_crypto_functions(lib_name)
            
            # Compile
            results = self.compiler.compile_library(
                library_name=lib_name,
                source_dir=source_dir,
                functions=functions,
                output_dir=str(self.output_dir / 'binaries' / lib_name)
            )
            
            all_results[lib_name] = results
        
        # Save compilation metadata
        self._save_metadata(all_results)
        
        logger.info("\n" + "="*60)
        logger.info("COMPILATION COMPLETE!")
        logger.info("="*60)
        
        total_binaries = sum(len(r) for r in all_results.values())
        logger.info(f"Total binaries compiled: {total_binaries}")
    
    def _get_crypto_functions(self, library: str) -> List[str]:
        """
        Get list of crypto functions to compile from library
        
        Args:
            library: Library name
        
        Returns:
            List of function names
        """
        # Map of library to its important crypto functions
        function_map = {
            'openssl': [
                'AES_encrypt', 'AES_decrypt', 'AES_set_encrypt_key',
                'RSA_public_encrypt', 'RSA_private_decrypt',
                'SHA256_Init', 'SHA256_Update', 'SHA256_Final',
                'SHA1_Init', 'SHA1_Update', 'SHA1_Final',
                'MD5_Init', 'MD5_Update', 'MD5_Final',
                'DES_encrypt1', 'DES_decrypt1',
                'HMAC', 'HMAC_Init', 'HMAC_Update', 'HMAC_Final'
            ],
            'mbedtls': [
                'mbedtls_aes_encrypt', 'mbedtls_aes_decrypt',
                'mbedtls_rsa_public', 'mbedtls_rsa_private',
                'mbedtls_sha256', 'mbedtls_sha1', 'mbedtls_md5',
                'mbedtls_des_crypt_ecb', 'mbedtls_des3_crypt_ecb'
            ],
            'libsodium': [
                'crypto_secretbox_easy', 'crypto_secretbox_open_easy',
                'crypto_box_easy', 'crypto_box_open_easy',
                'crypto_sign', 'crypto_sign_open',
                'crypto_hash_sha256', 'crypto_hash_sha512'
            ]
        }
        
        return function_map.get(library, [])
    
    def _save_metadata(self, results: Dict):
        """
        Save compilation metadata to JSON
        
        Args:
            results: Compilation results
        """
        metadata_file = self.output_dir / 'compilation_metadata.json'
        
        # Convert to serializable format
        serializable = {}
        for lib_name, lib_results in results.items():
            serializable[lib_name] = {}
            for key, value in lib_results.items():
                key_str = f"{key[0]}_{key[1]}_{key[2]}"
                serializable[lib_name][key_str] = value
        
        with open(metadata_file, 'w') as f:
            json.dump(serializable, f, indent=2)
        
        logger.info(f"Metadata saved to: {metadata_file}")


