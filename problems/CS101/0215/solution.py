import StudentClass

first, last = raw_input().split()
Test = StudentClass.Student(first, last)
print "%s, %s" % (Test.First, Test.Last)

