
def save_text_to_file(text, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        return True
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return False

if __name__ == '__main__':
    # 示例调用
    save_text_to_file("这是一个测试文本", "favordb.txt")