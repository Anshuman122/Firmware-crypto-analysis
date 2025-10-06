# Hinglish: Yeh dynamic analysis ka core logic hai, jo Unicorn Engine ka use karke code emulate karta hai.
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_PROT_ALL, UC_HOOK_CODE, UC_SECOND_SCALE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX
from typing import List, Dict, Any

from crypto_finder.common.logging import log

# Emulation ke liye memory addresses
BASE_ADDRESS = 0x1000000
STACK_ADDRESS = 0x3000000
STACK_SIZE = 1024 * 1024  # 1 MB stack

class DynamicRunner:
    """Unicorn Engine ka use karke machine code ko emulate karta hai."""

    def __init__(self, arch=UC_ARCH_X86, mode=UC_MODE_64):
        try:
            self.emulator = Uc(arch, mode)
            log.info(f"Unicorn emulator for arch={arch}, mode={mode} successfully initialized.")
        except UcError as e:
            log.error(f"Unicorn emulator initialize karne me fail: {e}")
            raise

    def _setup_memory(self, code: bytes):
        """Emulator ke liye memory map karta hai."""
        self.emulator.mem_map(BASE_ADDRESS, 4 * 1024 * 1024) # 4MB for code
        self.emulator.mem_map(STACK_ADDRESS, STACK_SIZE)
        
        # Machine code ko memory me write karo
        self.emulator.mem_write(BASE_ADDRESS, code)
        
        # Stack pointer (RSP) set karo
        self.emulator.reg_write(UC_X86_REG_RSP, STACK_ADDRESS + STACK_SIZE - 1)
        log.info("Emulator memory successfully setup.")

    def _trace_instruction(self, uc, address, size, user_data):
        """
        Har instruction execute hone par yeh function call hota hai (hook).
        """
        trace_list = user_data['trace']
        try:
            instruction_bytes = uc.mem_read(address, size)
            trace_list.append({
                "address": hex(address),
                "size": size,
                "bytes": instruction_bytes.hex()
            })
        except Exception:
            # Agar memory readable na ho to skip karo
            pass

    def emulate(self, code: bytes, entry_point: int = BASE_ADDRESS, instruction_limit: int = 1000) -> Dict[str, Any]:
        """
        Diye gaye machine code ko emulate karta hai aur trace generate karta hai.
        """
        log.info(f"Starting emulation at {hex(entry_point)} with instruction limit {instruction_limit}.")
        
        trace_data = {"trace": []}
        
        try:
            self._setup_memory(code)
            
            # Har instruction ko trace karne ke liye hook add karo
            hook = self.emulator.hook_add(UC_HOOK_CODE, self._trace_instruction, user_data=trace_data)
            
            # Emulation start karo
            self.emulator.emu_start(
                begin=entry_point,
                until=0, # End address (0 matlab end tak)
                timeout=5 * UC_SECOND_SCALE, # 5 second ka timeout
                count=instruction_limit # Max instructions
            )
            
            # Hook ko remove karo
            self.emulator.hook_del(hook)
            
            log.success("Emulation finished successfully.")
            return {
                "status": "success",
                "instruction_count": len(trace_data["trace"]),
                "trace": trace_data["trace"],
                "final_registers": {
                    "rax": hex(self.emulator.reg_read(UC_X86_REG_RAX)),
                    "rbx": hex(self.emulator.reg_read(UC_X86_REG_RBX)),
                    "rcx": hex(self.emulator.reg_read(UC_X86_REG_RCX)),
                    "rdx": hex(self.emulator.reg_read(UC_X86_REG_RDX)),
                }
            }
        except UcError as e:
            log.error(f"Emulation ke dauran error aaya: {e}")
            return {"status": "error", "message": str(e), "trace": trace_data["trace"]}