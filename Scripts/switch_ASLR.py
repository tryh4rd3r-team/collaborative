import os, sys, argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--enable", dest="enable_aslr", action="store_true", help="Disable ASLR")
    parser.add_argument("-d", "--disable", dest="disable_aslr", action="store_true", help="Enable ASLR")
    options = parser.parse_args()
    if not options.enable_aslr and not options.disable_aslr:
        parser.error("[-] Please specify the the action. use -h for help.")
    return options


options = get_arguments()

if options.enable_aslr:
    os.system("echo 2 | tee /proc/sys/kernel/randomize_va_space")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    print("\nASLR Enabled.\n")

if options.disable_aslr:
    os.system("echo 0 | tee /proc/sys/kernel/randomize_va_space")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    print("\nASLR Disabled.\n")