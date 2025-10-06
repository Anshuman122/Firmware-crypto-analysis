# Hinglish: Yeh ek IDAPython script hai jo IDA Pro ke andar chalti hai.
# Yeh current function ko analyze karne ke liye hamari API ko call karti hai.

import idaapi
import idc
import requests
import json

API_URL = "http://127.0.0.1:8000/api/v1/predict"

def analyze_function_with_api(func_ea):
    """Ek function ko API se analyze karta hai aur result ko comment me add karta hai."""
    
    func = idaapi.get_func(func_ea)
    if not func:
        print("Not a valid function address.")
        return

    func_name = idc.get_func_name(func_ea)
    print("Analyzing function: %s at 0x%x" % (func_name, func_ea))
    
    # IDA se function ke baare me data collect karo (yeh ek simple example hai)
    # Asli implementation me P-Code ya dusre features extract karne honge
    func_data = {
        "name": func_name,
        "size": func.end_ea - func.start_ea,
        "instruction_count": 0, # Placeholder
        "pcode": [] # Placeholder
    }
    
    try:
        response = requests.post(API_URL, json=func_data)
        response.raise_for_status()
        
        result = response.json()
        prediction = result.get('prediction', {})
        label = prediction.get('label')
        confidence = prediction.get('confidence')
        
        if label:
            comment = "Crypto Finder Prediction: %s (Confidence: %.2f)" % (label.upper(), confidence)
            print(comment)
            # Function ke start me comment add karo
            idc.set_func_cmt(func_ea, comment, 1)
        
    except requests.exceptions.RequestException as e:
        print("API ko call karne me error: %s" % e)

def main():
    # Current cursor address par jo function hai, usse analyze karo
    current_address = idc.get_screen_ea()
    func_address = idaapi.get_func(current_address).start_ea
    if func_address != idaapi.BADADDR:
        analyze_function_with_api(func_address)
    else:
        print("Please place your cursor inside a function.")

if __name__ == "__main__":
    main()