import os
import unittest
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Test(unittest.TestCase):
    def test_mode_1(self):
        self.assert_all_set('1', 'data/mode_1')

    def test_mode_2(self):
        self.assert_all_set('2', 'data/mode_2')

    def test_mode_3(self):
        self.assert_all_set('3', 'data/mode_3')

    def test_mode_4(self):
        self.assert_all_set('4', 'data/mode_4')

    def test_mode_7(self):
        self.assert_all_set('7', 'data/mode_7')

    def assert_all_set(self, mode, dir_path):
        for data_set_dir in os.listdir(dir_path):
            path = f'{dir_path}/{data_set_dir}'
            result = self.get_output(f'{path}/input.txt', mode)
            with open(f'{path}/output.txt', "r") as f:
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
