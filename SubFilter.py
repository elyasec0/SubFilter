import sys
import json
import argparse
from urllib.parse import urlparse, parse_qs

# دالة تحميل نتائج الأدوات بناءً على نوع الأداة
def load_tool_results(file_path, tool_type="subfinder"):
    """تحميل مخرجات أدوات subdomain بناءً على الأداة المختارة"""
    
    if tool_type == "amass":
        return load_amass_results(file_path)  # معالجة مخرجات Amass
    elif tool_type == "subfinder":
        return load_subfinder_results(file_path)  # معالجة مخرجات Subfinder
    elif tool_type == "sublist3r":
        return load_sublist3r_results(file_path)  # معالجة مخرجات Sublist3r
    elif tool_type == "aquatone":
        return load_aquatone_results(file_path)  # معالجة مخرجات Aquatone
    elif tool_type == "knockpy":
        return load_knockpy_results(file_path)  # معالجة مخرجات Knockpy
    else:
        raise ValueError(f"Unsupported tool type: {tool_type}")

def load_amass_results(file_path):
    """تحميل مخرجات Amass (JSON)"""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [entry['name'] for entry in data['hostnames']]

def load_subfinder_results(file_path):
    """تحميل مخرجات Subfinder (TXT)"""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def load_sublist3r_results(file_path):
    """تحميل مخرجات Sublist3r (TXT)"""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def load_aquatone_results(file_path):
    """تحميل مخرجات Aquatone (HTML أو CSV)"""
    pass

def load_knockpy_results(file_path):
    """تحميل مخرجات Knockpy (TXT)"""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# دالة تصفية الـ URLs بناءً على الأداة
def filter_urls(urls, tool_type="subfinder"):
    """تصفية الـ URLs بناءً على الأداة المستخدمة"""
    
    if tool_type in ["subfinder", "sublist3r", "knockpy"]:
        return filter_simple_urls(urls)  # إذا كانت الأداة تنتج ملف نصي بسيط
    elif tool_type == "amass":
        return filter_amass_urls(urls)  # إذا كانت الأداة تنتج ملف JSON
    elif tool_type == "aquatone":
        return filter_aquatone_urls(urls)  # إذا كانت الأداة تنتج HTML أو CSV
    else:
        raise ValueError(f"Unsupported tool type for filtering: {tool_type}")

def filter_simple_urls(urls):
    """تصفية الـ URLs البسيطة (نصية)"""
    seen = set()
    filtered = []
    
    for url in urls:
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        params = parse_qs(parsed.query)
        
        # تحويل parameters إلى tuple بدلاً من list لتجنب الخطأ
        params_tuple = tuple((key, tuple(value)) for key, value in params.items())
        
        # إزالة التكرار بناءً على الـ base_url + الـ parameters
        if (base_url, frozenset(params_tuple)) not in seen:
            filtered.append(url)
            seen.add((base_url, frozenset(params_tuple)))
    
    return filtered

def filter_amass_urls(urls):
    """تصفية الـ URLs الناتجة عن Amass (JSON)"""
    return set(urls)  # نموذج تصفية بسيط

def filter_aquatone_urls(urls):
    """تصفية الـ URLs الناتجة عن Aquatone (HTML أو CSV)"""
    return set(urls)  # نموذج تصفية بسيط

# دالة لحفظ الـ URLs المصفاة
def save_filtered_urls(filtered_urls, output_file="filtered_urls.txt"):
    """حفظ الـ URLs المصفاة إلى ملف نصي."""
    with open(output_file, 'w') as file:
        for url in filtered_urls:
            file.write(url + "\n")
    print(f"Filtered URLs saved to {output_file}")

# دالة التعامل مع واجهة سطر الأوامر
def main():
    parser = argparse.ArgumentParser(description="Filter subdomains from different tools.")
    parser.add_argument("input_file", help="Input file containing subdomains (from an external tool)")
    parser.add_argument("--tool", choices=["amass", "subfinder", "sublist3r", "aquatone", "knockpy"], required=True, help="Tool used to generate the subdomain list")
    parser.add_argument("--output", default="filtered_subdomains.txt", help="Output file to save filtered results")
    
    args = parser.parse_args()

    # تحميل المخرجات بناءً على نوع الأداة
    urls = load_tool_results(args.input_file, args.tool)

    # تصفية الـ URLs
    filtered_urls = filter_urls(urls, args.tool)

    # حفظ الـ URLs المصفاة
    save_filtered_urls(filtered_urls, args.output)

if __name__ == "__main__":
    main()
