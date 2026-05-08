from pathlib import Path

def main() -> int:
    base_dir = Path(__file__).resolve().parent
    input_file = base_dir / "input.txt"

    print("Nhap duong dan thu muc luu anh (SAVE_DIR).")
    save_dir = input("SAVE_DIR: ").strip().strip('"')

    if not save_dir:
        print("Loi: SAVE_DIR khong duoc de trong.")
        return 1

    if not input_file.exists():
        input_file.touch()
    input_file.write_text(save_dir, encoding="utf-8")
    print(f"Da luu SAVE_DIR vao: {input_file}")
    print("Nhấn phím Enter để tiếp tục...")
    input()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
