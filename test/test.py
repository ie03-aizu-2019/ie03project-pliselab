import os
import unittest
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Test(unittest.TestCase):
    def test_mode_1(self):
        result_1_1 = self.get_output("data/input/1_1.txt", "1")
        result_1_2 = self.get_output("data/input/1_2.txt", "1")
        result_1_3 = self.get_output("data/input/1_3.txt", "1")
        with open("data/output_t_1/1.txt", "r") as f1:
            expect1 = f1.read()
        with open("data/output_t_1/2.txt", "r") as f2:
            expect2 = f2.read()
        with open("data/output_t_1/3.txt", "r") as f3:
            expect3 = f3.read()
        self.assertEqual(result_1_1, expect1)
        self.assertEqual(result_1_2, expect2)
        self.assertEqual(result_1_3, expect3)
    
    def test_mode_2(self):
        result = self.get_output("data/input/2.txt", "2")
        with open("data/output_t_2/1.txt", "r") as f:
            expect = f.read()
        self.assertEqual(result, expect)

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
