import argparse
import os
from time import sleep
from thuonglib.encrypt_decrypt_file    import (encrypt_file as encrypt_file_XOR, 
                                               decrypt_file as decrypt_file_XOR, 
                                               encrypt_file_BASE64, 
                                               decrypt_file_BASE64)
from thuonglib.c_by_hand               import control_by_hand
from thuonglib.delete_folder           import clean_files_temp_files_recycleBin, del_dir_downloads
from thuonglib.password_cipher         import *
from thuonglib.divide_merge_file       import divide_file, merge_file
from thuonglib.AES_CBC                 import encrypt_file_AES_CBC, decrypt_file_AES_CBC
from thuonglib.RSA_OAEP                import (export_keys_RSA_OAEP, 
                                               encrypt_file as encrypt_file_rsa, 
                                               decrypt_file as decrypt_file_rsa, 
                                               encrypt_text_RSA, 
                                               decrypt_text_RSA)
from thuonglib.AES_CTR                 import encrypt_file_AES_CTR, decrypt_file_AES_CTR
from thuonglib.AES_GCM                 import encrypt_file_AES_GCM, decrypt_file_AES_GCM
from thuonglib.HASH                    import sha256, sha512, sha3_256, sha3_512, check_hash
from thuonglib.utilities               import (cipher_utilities,
                                               findPhraseInFiles,
                                               screen_capture_tool,
                                               cliHelp)
from thuonglib.fileSecurity            import file_Security, unFileSecurity
from thuonglib.file_compression        import compress_file_1, decompress_file_1
import gzip
from pathlib                           import Path

def main():
    parser = argparse.ArgumentParser(
        prog="cli",
        usage="\ncli [OPTIONS] COMMAND [ARGS_0] [ARGS_1] [ARGS_2]...\n",
        description="Chương trình điều khiển máy tính bằng dòng lệnh.\n"
                    "Chương trình được viết bởi Trần Đình Thương.\n"
                    "Email: qbquangbinh@gmail.com"
    )

    parser.add_argument("--time", "-t", type=int, default=0, help="Thời gian tắt máy / restart " \
                                                                  "máy / sleep (giây), ví dụ: -t 60")
    parser.add_argument("--version", action="version", version="Version 1.1.4", help="Show version information")
    parser.add_argument("--verbose", "-v", action="store_true", help="Hiển thị thông tin khi chương trình chạy")
    parser.add_argument("--delete", "-d", action="store_true", help="Lựa chon xóa file hoặc không")

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = False

    cipher_text_parser = subparsers.add_parser("cipher", help="Ma hoa van ban và giai ma bang XOR cipher, sau do luu vao files")

    XOR_file_parser = subparsers.add_parser("XOR", help="Mã hóa file và giải mã file bằng XOR cipher.")
    XOR_file_parser.add_argument("--encrypt_file", "-ef", action="store_true", help="Mã hóa file bằng XOR cipher.")
    XOR_file_parser.add_argument("--decrypt_file", "-df", action="store_true", help="Giải mã file bằng XOR cipher.")

    XOR_text_parser = subparsers.add_parser("XOR_TEXT", help="Mã hóa văn bản và giải mã văn bản bằng XOR cipher.")
    XOR_text_parser.add_argument("--encrypt_text", "-eft", action="store_true", help="Mã hóa văn bản bằng XOR cipher.")
    XOR_text_parser.add_argument("--decrypt_text", "-dft", action="store_true", help="Giải mã văn bản bằng XOR cipher.")

    RSA_text_parser = subparsers.add_parser("RSA_TEXT", help="Mã hóa văn bản và giải mã văn bản bằng Base64 và RSA.")
    RSA_text_parser.add_argument("--encrypt_text_rsa", "-eftrsa", action="store_true", help="Mã hóa văn bản bằng Base64 và RSA.")
    RSA_text_parser.add_argument("--decrypt_text_rsa", "-dftrsa", action="store_true", help="Giải mã văn bản bằng Base64 và RSA.")

    BASE64_file_parser = subparsers.add_parser("BASE64_FILE", help="Mã hóa file và giải mã file bằng base64.")
    BASE64_file_parser.add_argument("--encrypt", "-ef", action="store_true", help="Mã hóa file bằng base64.")
    BASE64_file_parser.add_argument("--decrypt", "-df", action="store_true", help="Giải mã file bằng base64.")

    AES_CBC_parser = subparsers.add_parser("AES_CBC", help="Chương trình mã hóa và giải mã file bằng AES-CBC. Lệnh hỗ trợ option (delete)")
    AES_CBC_parser.add_argument("--encrypt_file", "-ef", action="store_true", help="Mã hóa file bằng AES-CBC.")
    AES_CBC_parser.add_argument("--decrypt_file", "-df", action="store_true", help="Giải mã file bằng AES-CBC.")

    AES_CTR_parser = subparsers.add_parser("AES_CTR", help="Chương trình mã hóa và giải mã file bằng AES-CTR.")
    AES_CTR_parser.add_argument("--encrypt_file", "-ef", action="store_true", help="Mã hóa file bằng AES-CTR.")
    AES_CTR_parser.add_argument("--decrypt_file", "-df", action="store_true", help="Giải mã file bằng AES-CTR.")
    
    AES_GCM_parser = subparsers.add_parser("AES_GCM", help="Chương trình mã hóa và giải mã file bằng AES-GCM.")
    AES_GCM_parser.add_argument("--encrypt_file", "-ef", action="store_true", help="Mã hóa file bằng AES-GCM.")
    AES_GCM_parser.add_argument("--decrypt_file", "-df", action="store_true", help="Giải mã file bằng AES-GCM.")

    AES_RSA_parser = subparsers.add_parser("AES_RSA", help="Chương trình tạo khóa RSA, mã hóa và giải mã file bằng AES-CBC và RSA-OAEP.")
    AES_RSA_parser.add_argument("--generate_keys", "-gk", action="store_true", help="Tạo cặp khóa RSA (public và private).")
    AES_RSA_parser.add_argument("--encrypt_file", "-ef", action="store_true", help="Mã hóa file bằng AES-CBC và khóa RSA.")
    AES_RSA_parser.add_argument("--decrypt_file", "-df", action="store_true", help="Giải mã file bằng AES-CBC và khóa RSA.")
    
    hash_parser = subparsers.add_parser("hash", help="Tạo giá trị băm SHA256, SHA512, SHA3_256, SHA3_512 từ dữ liệu đầu vào.")
    hash_parser.add_argument("--algorithm", "-a", choices=["SHA256", "SHA512", "SHA3_256", "SHA3_512"], default="SHA3_512", 
                             help="Chọn thuật toán băm SHA256, SHA512, SHA3_256, SHA3_512 (mặc định là SHA3_512).")
    hash_parser.add_argument("data", type=str, 
                             help="Dữ liệu đầu vào để băm, chuỗi data hoặc chuỗi rỗng nếu tạo giá trị hash bằng với file.")
    
    check_hash_parser = subparsers.add_parser("check_hash", help="So sánh mã hash của file với mã hash đã cung cấp.")

    sign_file_parser = subparsers.add_parser("sign", help="Chương trình chữ ký số, dùng thư viện pycryptodome.")
    sign_file_parser.add_argument("--creat", "-cs", action="store_true", help="Tạo chữ ký số.")
    sign_file_parser.add_argument("--verify", "-vs", action="store_true", help="Xác minh chữ ký số.")
    sign_file_parser.add_argument("--filePath", "-fp", required=True, type=str, help="Đường dẫn file cần tạo hoặc xác minh chữ ký số.", metavar="INFILE")
    sign_file_parser.add_argument("--keyPath", "-kp", required=True, type=str, 
                                  help="Đường dẫn đến khóa riêng tư (để tạo chữ ký số) hoặc khóa công khai (để xác minh chữ ký số).", metavar="INFILE")
    sign_file_parser.add_argument("--passworldKey", "-pk", required=True, type=bool, help="Nhập True hoặc False, mật khẩu để bảo vệ khóa RSA.", 
                                  metavar="True/False")
    
    file_security_parser = subparsers.add_parser("file", help="Chương trình mã hóa và chữ ký số, dùng thư viện pycryptodome.")
    file_security_parser.add_argument("--choice", "-ch", choices=["ENC", "DEC"], help="Chọn ENC để mã hóa, DEC để giải mã.")
    file_security_parser.add_argument("--filePath", "-fp", required=True, type=str, help="Đường dẫn file cần tạo hoặc xác minh chữ ký số.", metavar="INFILE")
    file_security_parser.add_argument("--privateKeyPath", "-pri", required=True, type=str, help="Đường dẫn đến khóa riêng.", metavar="INFILE")
    file_security_parser.add_argument("--passKeyPrivate", "-p_pri", required=True, type=bool, help="Nhập True hoặc False.", metavar="True/False")
    file_security_parser.add_argument("--publicKeyPath", "-pub", required=True, type=str, help="Đường dẫn đến khóa công khai.", metavar="INFILE")
    file_security_parser.add_argument("--passKeyPublic", "-p_pub", required=True, type=bool, help="Nhập True hoặc False.", metavar="True/False")

    compress_file_1_parser = subparsers.add_parser("compress_file_1", help="Chương trình nén file bằng thuật toán Huffman.")
    compress_file_1_parser.add_argument("--choice", "-c", choices=["com", "decom"], required=True, 
                                        help="Chọn 'com' để nén file, 'decom' để giải nén file.")
    compress_file_1_parser.add_argument("--input_file", "-i", type=str, required=True, 
                                        help="Đường dẫn file đầu vào để nén hoặc giải nén.", metavar="INFILE")
    
    compress_file_2_parser = subparsers.add_parser("gzip", help="Chương trình nén file bằng gzip.")
    compress_file_2_parser.add_argument("--choice", "-c", choices=["com", "decom"], required=True, 
                                        help="Chọn 'com' để nén file, 'decom' để giải nén file.")
    compress_file_2_parser.add_argument("--input_file", "-i", type=str, required=True, 
                                        help="Đường dẫn file đầu vào để nén hoặc giải nén.", metavar="INFILE")
    
    find_phrase_in_files_parser = subparsers.add_parser("findPhrase", 
                                                        help="Tìm một cụm từ trong tất cả file bên trong một thư mục,"
                                                             " kể cả thư mục con.\n"
                                                             "Ví dụ chạy lệnh: cli findPhrase")
    find_phrase_in_files_parser.add_argument("--encoding", type=str, default="utf-8", required=False, 
                                                                                            help="Chọn bảng mã như utf-8,..."
                                                                                                 ", mặc định utf-8")
    
    screen_capture_tool_parser = subparsers.add_parser("cap",
                                                       help="Chụp ảnh màn hình")
    
    shutdown_parser = subparsers.add_parser("shutdown",
                                             help="Tắt máy tính")
    
    restart_parser = subparsers.add_parser("restart",
                                            help="Khởi động lại máy tính")
    
    sleep_parser = subparsers.add_parser("sleep",
                                          help="Đưa máy tính vào chế độ ngủ")
    
    clean_parser = subparsers.add_parser("clean",
                                          help=r"Xóa file ở thư mục tạm (C:\) và file ở thùng rác")
    
    div_mer_file_parser = subparsers.add_parser("div_mer_file",
                                          help="Chia và ghép file")
    
    printHelp_parser = subparsers.add_parser("printHelp",
                                             help="Hiển thị trợ giúp")
    
    args = parser.parse_args()
    print_var = f'''

    Hello, Trần Đình Thương!
    Chương trình điều khiển máy tính bằng dòng lệnh
    Chương trình được viết bởi Trần Đình Thương
    Email: qbquangbinh@gmail.com

'''
    print(print_var)
    if args.command == "shutdown":
        shutdown_time = max(0, args.time)
        if shutdown_time:
            print(f"Máy tính sẽ tắt sau {shutdown_time} s")
            sleep(5)
        os.system(f"shutdown /s /t {shutdown_time}")
    elif args.command == "restart":
        restart_time = max(0, args.time)
        if restart_time:
            print(f"Máy tính sẽ restart sau {restart_time} s")
            sleep(5)
        os.system(f"shutdown /r /t {restart_time}")
    elif args.command == "sleep":
        sleep_time = max(0, args.time)
        if sleep_time > 0:
            print(f"Máy tính sẽ sleep sau {sleep_time} s")
            sleep(5)
            os.system(f"timeout /t {sleep_time} /nobreak > nul && rundll32.exe powrprof.dll,SetSuspendState 1,1,1")
        else:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 1,1,1")
    elif args.command == "clean":
        clean_files_temp_files_recycleBin()
        
    elif args.command == "XOR_TEXT":
        if args.encrypt_text:
            encrypt_text_XOR()
        elif args.decrypt_text:
            decrypt_text_XOR()
    elif args.command == "cipher":
        INPUT_FILE = Path(__file__).resolve().with_name("configForFuntionP_cipher.txt")
        p_cipher(str(INPUT_FILE))
    elif args.command == "XOR":
        if args.encrypt_file:
            encrypt_file_XOR()
        elif args.decrypt_file:
            decrypt_file_XOR()
    elif args.command == "div_mer_file":
        print("Chia va ghep file.")
        choice = input("Nhap lua chon cua ban (d/m): ").lower()
        while choice not in ['d', 'm']:
            choice = input("Nhap 'd' de chia file, 'm' de ghep file: ").lower()
        if choice == 'd':
            divide_file()
        else:
            merge_file()
    elif args.command == "AES_CBC":
        if args.encrypt_file:
            encrypt_file_AES_CBC(args.delete)
        elif args.decrypt_file:
            decrypt_file_AES_CBC(delete = args.delete)
    elif args.command == "RSA_TEXT":
        INPUT_FILE = Path(__file__).resolve().with_name("configForKey_RSA_OAEP.yaml")
        if args.encrypt_text_rsa:
            encrypt_text_RSA(str(INPUT_FILE))
        elif args.decrypt_text_rsa:
            decrypt_text_RSA(str(INPUT_FILE))
    elif args.command == "BASE64_FILE":
        if args.encrypt:
            encrypt_file_BASE64()
        elif args.decrypt:
            decrypt_file_BASE64()
    elif args.command == "AES_RSA":
        INPUT_FILE = Path(__file__).resolve().with_name("configForKey_RSA_OAEP.yaml")
        if args.generate_keys:
            export_keys_RSA_OAEP(str(INPUT_FILE))
        elif args.encrypt_file:
            encrypt_file_rsa(file = str(INPUT_FILE), init_key = 0, delete = args.delete)
        elif args.decrypt_file:
            decrypt_file_rsa(file = str(INPUT_FILE), init_key = 0, delete = args.delete)
    elif args.command == "AES_CTR":
        if args.encrypt_file:
            encrypt_file_AES_CTR()
        elif args.decrypt_file:
            decrypt_file_AES_CTR()
    elif args.command == "AES_GCM":
        if args.encrypt_file:
            encrypt_file_AES_GCM()
        elif args.decrypt_file:
            decrypt_file_AES_GCM()
    elif args.command == "hash":
        if args.algorithm == "SHA256":
            sha256(args.data, file_write=0 if args.data else 1)
        elif args.algorithm == "SHA512":
            sha512(args.data, file_write=0 if args.data else 1)
        elif args.algorithm == "SHA3_256":
            sha3_256(args.data, file_write=0 if args.data else 1)
        elif args.algorithm == "SHA3_512":
            sha3_512(args.data, file_write=0 if args.data else 1)
    elif args.command == "check_hash":
        check_hash()
    elif args.command == "sign":
        if args.creat:
            cipher_utilities.sign_file(args.filePath, args.keyPath, args.passworldKey)
        elif args.verify:
            cipher_utilities.verify_signature(args.filePath, args.keyPath)
    elif args.command == "file":
        if args.choice == "ENC":
            file_Security(args.filePath, args.privateKeyPath, args.passKeyPrivate, args.publicKeyPath, args.passKeyPublic)
        elif args.choice == "DEC":
            unFileSecurity(args.filePath, args.privateKeyPath, args.passKeyPrivate, args.publicKeyPath, args.passKeyPublic)
    elif args.command == "compress_file_1":
        if args.choice == "com":
            compress_file_1(args.input_file)
        elif args.choice == "decom":
            decompress_file_1(args.input_file)
    elif args.command == "gzip":
        p = Path(args.input_file)
        if not p.exists():
            print(f"File {args.input_file} không tồn tại.")
            return
        if args.choice == "com":
            out_path = p.with_name('gz_' + p.name + '.gz')
            with open(args.input_file, 'rb') as f_in, gzip.open(out_path, 'wb') as f_out:
                f_out.writelines(f_in)
            print(f"File {args.input_file} đã được nén thành {out_path}")
        elif args.choice == "decom":
            if not args.input_file.endswith('.gz'):
                print("Vui lòng cung cấp file nén gzip (.gz).")
                return
            out_path = p.with_suffix('')
            with gzip.open(args.input_file, 'rb') as f_in, open(out_path, 'wb') as f_out:
                f_out.write(f_in.read())
            print(f"File {args.input_file} đã được giải nén thành {out_path}")

    elif args.command == "findPhrase":
        findPhraseInFiles(encoding=args.encoding)

    elif args.command == "cap":
        INPUT_FILE = Path(__file__).resolve().with_name("capture_once.bat")
        screen_capture_tool(str(INPUT_FILE), args.verbose)
    elif args.command == "printHelp":
        INPUT_FILE = Path(__file__).resolve().with_name("help.txt")
        cliHelp(str(INPUT_FILE))
    else:
        INPUT_FILE = Path(__file__).resolve().with_name("help.txt")
        cliHelp(str(INPUT_FILE))

if __name__ == "__main__":
    main()
