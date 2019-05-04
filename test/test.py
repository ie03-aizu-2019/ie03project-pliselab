import os
import unittest
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Test(unittest.TestCase):
    def test_mode_3(self):
        result = self.get_output("data/input/3.txt", "3")
        with open("data/output_t_3/3.txt", "r") as f:
            expect = f.read()
        self.assertEqual(result, expect)

    def test_mode_4(self):
        result = self.get_output("data/input/3.txt", "4")
        with open("data/output_t_4/3.txt", "r") as f:
            expect = f.read()
        self.assertEqual(result, expect)

    def get_output(self, filepath, mode):
        """main.pyを実行し出力を返す

        Args:
            filepath (str): 標準入力に使用するファイルのパス
            mode (str): モード

        Returns:
            str: 出力
        """
        p = subprocess.Popen(["cat", filepath], stdout=subprocess.PIPE)
        p.wait()
        res = subprocess.check_output(
            ["python3", "../source/main.py", "-m", mode], stdin=p.stdout)
        p.stdout.close()
        return res.decode("utf8")


if __name__ == "__main__":
    unittest.main()
