#!/usr/bin/env python3
from __future__ import print_function
import argparse
import re
import sys
import socket
import binascii
import datetime
import socks
import requests
import colorama
import zipfile
import os
import win_inet_pton
import platform
from colorama import Fore, Style
from DNSDumpsterAPI import DNSDumpsterAPI
import dns.resolver

colorama.init(Style.BRIGHT)


def print_out(data, end='\n'):
    print(Style.NORMAL + re.sub(' +', ' ', data) + Style.RESET_ALL,' ', end=end)


def ip_in_subnetwork(ip_address, subnetwork):
    (ip_integer, version1) = ip_to_integer(ip_address)
    (ip_lower, ip_upper, version2) = subnetwork_to_ip_range(subnetwork)

    if version1 != version2:
        raise ValueError("incompatible IP versions")

    return (ip_lower <= ip_integer <= ip_upper)


def ip_to_integer(ip_address):
    # try parsing the IP address first as IPv4, then as IPv6
    for version in (socket.AF_INET, socket.AF_INET6):
        try:
            ip_hex = win_inet_pton.inet_pton(version, ip_address) if platform == 'Windows' else socket.inet_pton(version, ip_address)
            ip_integer = int(binascii.hexlify(ip_hex), 16)

            return ip_integer, 4 if version == socket.AF_INET else 6
        except:
            pass

    raise ValueError("invalid IP address")


def subnetwork_to_ip_range(subnetwork):
    try:
        fragments = subnetwork.split('/')
        network_prefix = fragments[0]
        netmask_len = int(fragments[1])

        # try parsing the subnetwork first as IPv4, then as IPv6
        for version in (socket.AF_INET, socket.AF_INET6):

            ip_len = 32 if version == socket.AF_INET else 128

            try:
                suffix_mask = (1 << (ip_len - netmask_len)) - 1
                netmask = ((1 << ip_len) - 1) - suffix_mask
                ip_hex = socket.inet_pton(version, network_prefix)
                ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask
                ip_upper = ip_lower + suffix_mask

                return (ip_lower,
                        ip_upper,
                        4 if version == socket.AF_INET else 6)
            except:
                pass
    except:
        pass

    raise ValueError("invalid subnetwork")


def dnsdumpster(target):
    

    res = DNSDumpsterAPI(False).search(target)

    if res['dns_records']['host']:
        for entry in res['dns_records']['host']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print_out(
                    Style.BRIGHT + Fore.WHITE + "[FOUND:HOST] " + Fore.GREEN + "{domain} {ip} {as} {provider} {country}".format(
                        **entry))

    if res['dns_records']['dns']:
        for entry in res['dns_records']['dns']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print_out(
                    Style.BRIGHT + Fore.WHITE + "[FOUND:DNS] " + Fore.GREEN + "{domain} {ip} {as} {provider} {country}".format(
                        **entry))

    if res['dns_records']['mx']:
        for entry in res['dns_records']['mx']:
            provider = str(entry['provider'])
            if "Cloudflare" not in provider:
                print_out(
                    Style.BRIGHT + Fore.WHITE + "[FOUND:MX] " + Fore.GREEN + "{ip} {as} {provider} {domain}".format(
                        **entry))


def crimeflare(target):
    

    with open("data/ipout", "r") as ins:
        crimeFoundArray = []
        for line in ins:
            lineExploded = line.split(" ")
            if lineExploded[1] == args.target:
                crimeFoundArray.append(lineExploded[2])
            else:
                continue
    if (len(crimeFoundArray) != 0):
        for foundIp in crimeFoundArray:
            print_out(Style.BRIGHT + Fore.WHITE + "[FOUND:IP] " + Fore.GREEN + "" + foundIp.strip())
    else:
        print("Did not find anything")
        


def init(target):

    if not os.path.isfile("data/ipout"):
            print_out(Fore.CYAN + "No ipout file found, fetching data")
            update()
            print_out(Fore.CYAN + "ipout file created")

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print_out(Fore.RED + "Domain is not valid, exiting")
        sys.exit(0)

    print_out(Fore.CYAN + "Server IP: " + ip)

    try:
        ifIpIsWithin = inCloudFlare(ip)

        if ifIpIsWithin:
            print_out(Style.BRIGHT + Fore.GREEN + args.target + " is part of the Cloudflare network!")
        else:
            print_out(Fore.RED + args.target + " is not part of the Cloudflare network, quitting...")
            sys.exit(0)
    except ValueError:
        print_out(Fore.RED + "IP address does not appear to be within Cloudflare range.")
        sys.exit(0)


def inCloudFlare(ip):
    with open('{}/data/cf-subnet.txt'.format(os.getcwd())) as f:
        for line in f:
            isInNetwork = ip_in_subnetwork(ip, line)
            if isInNetwork:
                return True
        return False

def check_for_wildcard(target):
    
    return False

def subdomain_scan(target, subdomains):
    i = 0
    c = 0
    if check_for_wildcard(target):
        #If has wildcard or input N, return
        print_out(Fore.CYAN + "Scanning finished...")
        return

    if subdomains:
        subdomainsList = subdomains
    else:
        subdomainsList = "subdomains.txt"
    try:
        with open("data/" + subdomainsList, "r") as wordlist:
            numOfLines = len(open("data/subdomains.txt").readlines())
            numOfLinesInt = numOfLines
            numOfLines = str(numOfLines)
            print_out(Fore.CYAN + "Scanning " + numOfLines + " subdomains (" + subdomainsList + "), please wait...")
            for word in wordlist:
                c += 1
                if (c % int((float(numOfLinesInt) / 100.0))) == 0:
                    print_out(Fore.CYAN + str(round((c / float(numOfLinesInt)) * 100.0, 2)) + "% complete", '\r')

                subdomain = "{}.{}".format(word.strip(), target)
                try:
                    target_http = requests.get("http://" + subdomain)
                    target_http = str(target_http.status_code)
                    ip = socket.gethostbyname(subdomain)
                    ifIpIsWithin = inCloudFlare(ip)

                    if not ifIpIsWithin:
                        i += 1
                        print_out(
                            Style.BRIGHT + Fore.WHITE + "**HOST:** " + Fore.GREEN + subdomain + " IP: " + ip + " HTTP: " + target_http)
                    else:
                        print_out(
                            Style.BRIGHT + Fore.WHITE + "**SUBDOMAIN:** " + Fore.RED + subdomain + " ON CLOUDFLARE NETWORK!")
                        continue

                except requests.exceptions.RequestException as e:
                    continue
            if (i == 0):
                print_out(Fore.CYAN + "Scanning finished, we did not find anything, sorry...")
            else:
                print_out(Fore.CYAN + "Scanning finished...")

    except IOError:
        print_out(Fore.RED + "Subdomains file does not exist in data directory, aborting scan...")
        sys.exit(1)

def update():
    print_out(Fore.CYAN + "Just checking for updates, please wait...")
    print_out(Fore.CYAN + "Updating CloudFlare subnet...")
    if(args.tor == False):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'}
        r = requests.get("https://www.cloudflare.com/ips-v4", headers=headers, cookies={'__cfduid': "d7c6a0ce9257406ea38be0156aa1ea7a21490639772"}, stream=True)
        with open('data/cf-subnet.txt', 'wb') as fd:
            for chunk in r.iter_content(4000):
                fd.write(chunk)
    else:
        print_out(Fore.RED + Style.BRIGHT+"Unable to fetch CloudFlare subnet while TOR is active")
    print_out(Fore.CYAN + "Updating Crimeflare database...")
    r = requests.get("http://crimeflare.net:83/domains/ipout.zip", stream=True)
    with open('data/ipout.zip', 'wb') as fd:
        for chunk in r.iter_content(4000):
            fd.write(chunk)
    zip_ref = zipfile.ZipFile("data/ipout.zip", 'r')
    zip_ref.extractall("data/")
    zip_ref.close()
    os.remove("data/ipout.zip")


# END FUNCTIONS

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", help="target url of website", type=str)
parser.add_argument("-T", "--tor", dest="tor", action="store_true", help="enable TOR routing")
parser.add_argument("-u", "--update", dest="update", action="store_true", help="update databases")
parser.add_argument("-s", "--subdomains", help="name of alternate subdomains list stored in the data directory", type=str)
parser.set_defaults(tor=False)
parser.set_defaults(update=False)

args = parser.parse_args()

if args.tor is True:
    ipcheck_url = 'http://ipinfo.io/ip'
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
    socket.socket = socks.socksocket
    try:
        tor_ip = requests.get(ipcheck_url)
        tor_ip = str(tor_ip.text)

        print_out(Fore.WHITE + Style.BRIGHT + "TOR connection established!")
        print_out(Fore.WHITE + Style.BRIGHT + "New IP: " + tor_ip)

    except requests.exceptions.RequestException as e:
        sys.exit(0)

if args.update is True:
    update()

try:

    # Initialize CloudFail
    init(args.target)

    # Scan DNSdumpster.com
    dnsdumpster(args.target)

    # Scan Crimeflare database
    crimeflare(args.target)

    # Scan subdomains with or without TOR
    subdomain_scan(args.target, args.subdomains)

except KeyboardInterrupt:
    sys.exit(0)

#test
