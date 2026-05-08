# cli

`cli` là công cụ dòng lệnh (CLI) điều khiển máy tính và xử lý tệp, bao gồm:
- Mã hóa/giải mã tệp và văn bản.
- Băm dữ liệu (hash) và kiểm tra hash.
- Ký số/xác minh chữ ký số.
- Nén/giải nén tệp.
- Một số tiện ích hệ thống như chụp màn hình, dọn rác, tắt máy, khởi động lại, sleep.

Dự án được phát triển bởi **Trần Đình Thương**.

## Thông tin gói

- Tên package: `thuongcli`
- Phiên bản: `1.1.4`
- Python yêu cầu: `>=3.10.6`
- Entry point CLI: `cli=thuongcli.thuongcli:main`
- Repository: <https://github.com/qbquangb/cli>

## Phụ thuộc

Chương trình viết bằng ngôn ngữ **Python** và sử dụng các thư viện sau:
- `thuonglib`
- `pycryptodome`
- `numpy`
- `pillow`

## Cài đặt

Bước 1: Cài đặt Python 3.10.6 hoặc mới hơn trước khi cài `thuongcli`: <https://www.python.org/>.

Bước 2: Cài đặt `thuongcli`: Cài từ PyPI bằng pip (Mở terminal hoặc command prompt):

```bash
pip install thuongcli
```

## Cách dùng

Mở terminal hoặc command prompt và gõ `cli` để bắt đầu sử dụng.

Cú pháp tổng quát:

```bash
cli [OPTIONS] COMMAND [ARGS_0] [ARGS_1] [ARGS_2]...
```

Hiển thị trợ giúp:

```bash
cli printHelp
```

## Options (toàn cục)

- `--version`: Hiển thị phiên bản CLI và thoát.
- `-v, --verbose`: Hiển thị thông tin chi tiết hơn khi chạy lệnh.
- `-t, --time`: Thời gian (giây) cho các lệnh `shutdown`, `restart`, `sleep`. Ví dụ: `-t 60`.
- `-d, --delete`: Tùy chọn xóa file gốc sau khi mã hóa/giải mã (chỉ áp dụng cho lệnh có hỗ trợ).

## Commands

### 1. Nhóm mã hóa/giải mã

- `cipher`: Mã hóa/giải mã văn bản bằng XOR và lưu vào file.

```bash
cli cipher
```

- `XOR`: Mã hóa/giải mã file bằng XOR cipher.

```bash
cli XOR -ef   # mã hóa file
cli XOR -df   # giải mã file
```

- `XOR_TEXT`: Mã hóa/giải mã văn bản bằng XOR cipher.

```bash
cli XOR_TEXT -eft   # mã hóa văn bản
cli XOR_TEXT -dft   # giải mã văn bản
```

- `RSA_TEXT`: Mã hóa/giải mã văn bản bằng Base64 và RSA.

```bash
cli RSA_TEXT -eftrsa   # mã hóa văn bản
cli RSA_TEXT -dftrsa   # giải mã văn bản
```

- `BASE64_FILE`: Mã hóa/giải mã file bằng Base64.

```bash
cli BASE64_FILE -ef   # mã hóa file
cli BASE64_FILE -df   # giải mã file
```

- `AES_CBC`: Mã hóa/giải mã file bằng AES-CBC.

```bash
cli AES_CBC -ef        # mã hóa file
cli AES_CBC -df        # giải mã file
cli -d AES_CBC -ef     # mã hóa và xóa file gốc (nếu hỗ trợ)
```

- `AES_CTR`: Mã hóa/giải mã file bằng AES-CTR.

```bash
cli AES_CTR -ef   # mã hóa file
cli AES_CTR -df   # giải mã file
```

- `AES_GCM`: Mã hóa/giải mã file bằng AES-GCM.

```bash
cli AES_GCM -ef   # mã hóa file
cli AES_GCM -df   # giải mã file
```

- `AES_RSA`: Tạo khóa RSA, mã hóa/giải mã file bằng AES-CBC + RSA-OAEP.

```bash
cli AES_RSA -gk   # tạo cặp khóa RSA
cli AES_RSA -ef   # mã hóa file
cli AES_RSA -df   # giải mã file
```

### 2. Nhóm hash và kiểm tra toàn vẹn

- `hash`: Tạo giá trị băm SHA256, SHA512, SHA3_256, SHA3_512.

```bash
cli hash "noi_dung_can_bam"
cli hash -a SHA256 "noi_dung_can_bam"
cli hash -a SHA512 "noi_dung_can_bam"
cli hash -a SHA3_256 "noi_dung_can_bam"
cli hash -a SHA3_512 "noi_dung_can_bam"
```

- `check_hash`: So sánh mã hash của file với mã hash đã cung cấp.

```bash
cli check_hash
```

### 3. Nhóm chữ ký số và bảo mật file

- `sign`: Tạo và xác minh chữ ký số.

```bash
cli sign -cs --filePath INFILE --keyPath INFILE --passworldKey True   # tạo chữ ký số
cli sign -vs --filePath INFILE --keyPath INFILE --passworldKey True   # xác minh chữ ký số
```

- `file`: Mã hóa/giải mã file kết hợp chữ ký số.

```bash
cli file -ch ENC --filePath INFILE --privateKeyPath INFILE --passKeyPrivate True --publicKeyPath INFILE --passKeyPublic True
cli file -ch DEC --filePath INFILE --privateKeyPath INFILE --passKeyPrivate True --publicKeyPath INFILE --passKeyPublic True
```

### 4. Nhóm nén/giải nén tệp

- `compress_file_1`: Nén/giải nén bằng thuật toán Huffman.

```bash
cli compress_file_1 -c com -i INFILE      # nén file
cli compress_file_1 -c decom -i INFILE    # giải nén file
```

- `gzip`: Nén/giải nén bằng gzip.

```bash
cli gzip -c com -i INFILE      # nén file
cli gzip -c decom -i INFILE    # giải nén file .gz
```

### 5. Nhóm tiện ích hệ thống

- `findPhrase`: Tìm cụm từ trong toàn bộ file của thư mục (kể cả thư mục con).

```bash
cli findPhrase
cli findPhrase --encoding utf-8
```

- `cap`: Chụp ảnh màn hình.

```bash
cli cap
cli -v cap
```

- `div_mer_file`: Chia file hoặc ghép file.

```bash
cli div_mer_file
```

- `clean`: Xóa file ở thư mục tạm và thùng rác.

```bash
cli clean
```

- `shutdown`: Tắt máy tính.

```bash
cli shutdown
cli -t 60 shutdown
```

- `restart`: Khởi động lại máy tính.

```bash
cli restart
cli -t 60 restart
```

- `sleep`: Đưa máy tính vào chế độ ngủ.

```bash
cli sleep
cli -t 60 sleep
```

- `printHelp`: Hiển thị nội dung trợ giúp từ file `help.txt`.

```bash
cli printHelp
```

## Lưu ý sử dụng

- Với các lệnh mã hóa/giải mã, cần kiểm tra đúng input/key/cấu hình trước khi xử lý file quan trọng.
- Với các lệnh liên qua đến file nên sao lưu file trước khi thực thi lệnh, lúc thực thi thành công hoặc làm việc quen với lệnh mới thực thi trực tiếp (không cần sao lưu)

## Liên hệ

Nếu bạn cần hỗ trợ hoặc góp ý:

- Name: Trần Đình Thương
- Email: qbquangbinh@gmail.com
- Number Phone: 0335 652 338
