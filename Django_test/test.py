import unittest
import sys
sys.path.append('..')
sys.path.append('Django_test/module')
from Django_test.module import Calculator   # from 包名.文件名 import 类名


class ModuleTest(unittest.TestCase):
    def setUp(self):
        self.cal = Calculator(8, 4)

    def tearDown(self):
        pass

    def test_add(self):
        result = self.cal.add()
        self.assertEqual(result, 12)

    def test_sub(self):
        result = self.cal.sub()
        self.assertEqual(result, 4)

    def test_mul(self):
        result = self.cal.mul()
        self.assertEqual(result, 32)

    def test_div(self):
        result = self.cal.div()
        self.assertEqual(result, 2)


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(ModuleTest("test_add"))
    suite.addTest(ModuleTest("test_sub"))
    suite.addTest(ModuleTest("test_mul"))
    suite.addTest(ModuleTest("test_div"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
