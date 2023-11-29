from exif import Image
import argparse
import binascii
import re


def main():
    #the flags take in the file location that will be checked
    parser = argparse.ArgumentParser(description='Welcome to inspectore image')
    parser.add_argument("-map", dest="picture_location", help="location found in the image metadata")
    parser.add_argument("-steg", dest="PGP_key", help="prints out the public PGP key of current image")

    args = parser.parse_args()

    if args.picture_location != None:
        printImageLocation(args.picture_location)
        return
    if args.PGP_key != None:
        print_PGP_key(args.PGP_key)
        return
    print("Welcome to inspectore image\n use either -map or -steg + path/to/file to display information about the image")


def printImageLocation(fileLocation):
    #this function will try to read the file`s location from the metadata and then print it
    try:
        with open(fileLocation, 'rb') as image_file:
            my_image = Image(image_file)
            raw_latitude = my_image.get("gps_latitude")
            raw_longitude = my_image.get("gps_longitude")
    except FileNotFoundError:
        print("Could not find the file specified")
        return
    
    calculated_latitude = raw_latitude[0] + raw_latitude[1]/60+ raw_latitude[2]/3600
    calculated_longitude = raw_longitude[0] + raw_longitude[1]/60+ raw_longitude[2]/3600
    print("Lat/Lon:     (" + str(calculated_latitude) + ") / (" + str(calculated_longitude) +")")


def print_PGP_key(file_path):
    #this fuction takes in the file path and reads the file, then it convert it from binary into ascii
    #then it calls the extract_pgp function extract the the key.Then it gets foramted and printed
    with open(file_path, 'rb') as file:
        content = file.read()
        hex_strings = binascii.hexlify(content).decode('utf-8')
        
        # Split the hex string into chunks of 2 characters (bytes)
        byte_chunks = [hex_strings[i:i+2] for i in range(0, len(hex_strings), 2)]

        # Convert hex bytes to ASCII characters
        ascii_strings = ''.join([chr(int(chunk, 16)) for chunk in byte_chunks if 32 <= int(chunk, 16) <= 126])

    key = extract_pgp_key(ascii_strings)
    temp = "\n".join(key.split())

    print("-----BEGIN PGP PUBLIC KEY BLOCK-----\n"+temp+"\n-----END PGP PUBLIC KEY BLOCK-----")

def extract_pgp_key(input_string):
    pattern = re.compile(r'-----BEGIN PGP PUBLIC KEY BLOCK-----(.*?)-----END PGP PUBLIC KEY BLOCK-----', re.DOTALL)
    match = pattern.search(input_string)

    if match:
        pgp_key = match.group(1).strip()
        return pgp_key
    else:
        return None
    
main()