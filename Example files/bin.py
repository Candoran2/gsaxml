import json;
import sys;
import os;

# get first argument
arg = sys.argv[1];

endian = "big";

# reading shortcuts
r_int = lambda file, length: int.from_bytes(file.read(length), byteorder=endian);
# parse string to int

r_str = lambda file, length: file.read(length).decode("utf-8");
def r_str_null(file):
    # read string until null byte
    str = "";
    while True:
        byte = file.read(1);
        if byte == b"\x00":
            break;
        str += byte.decode("utf-8");
    return str;

r_bytes = lambda file, length: file.read(length);
move = lambda file, amount: file.seek(file.tell() + amount);

# seperate into id - accepts bytes and returns a string of the bytes seperated by a comma
def seperate_into_id(bytes):
    # convert bytes to string
    str = bytes.hex();
    # seperate into id
    id = "";
    for i in range(0, len(str), 2):
        id += str[i:i+2] + ",";
    # remove last comma
    id = id[:-1];
    return id;


def decompile():
    # decompile file to json
    # read file
    with open(arg, "rb") as gsa:
        # read the first 4 bytes as an int
        gsa.seek(0);
        str_tbl_len = r_int(gsa, 4);
        data = {};
        element_amount = 0;
        # read the string table
        while gsa.tell() < str_tbl_len:
            while gsa.tell() % 4 != 0:
                move(gsa, 1);
            move(gsa, 2);
            if gsa.tell() >= str_tbl_len:
                break;
            # read the string
            str = r_str_null(gsa);
            # add the string to the string table
            entry = {};
            # add the string to the entry
            entry["string"] = str;
            # add the entry to the data
            data[element_amount] = entry;
            print(str)
            # increment the element amount
            element_amount += 1;
        # seek to the end of the string table
        gsa.seek(str_tbl_len);
        # link id = 16 bytes
        link_id = r_bytes(gsa, 16);
        # convert link id to string
        link_id = seperate_into_id(link_id);
        print(link_id);
        gsa.seek(str_tbl_len + 16);
        for i in range(element_amount):
            # read the guid
            guid = r_bytes(gsa, 4);
            # convert guid to string
            guid = seperate_into_id(guid);
            # add the guid to the entry
            data[i]["guid"] = guid;

            print(guid);
        # print current position
        print(hex(gsa.tell()));
        # dump data to json
        with open(os.path.splitext(arg)[0] + ".json", "w") as json_file:
            json.dump(data, json_file, indent=4);
            


decompile();