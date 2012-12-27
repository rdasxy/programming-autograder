from solution import c2f, f2c

degC = float(raw_input("Enter a temperature in degree Celsius "))
print("%.2f degrees Celsius is %.2f degrees Fahrenheit" %(degC, c2f(degC)))
degF = float(raw_input("Enter a temperature in degree Fahrenheit "))
print("%.2f degrees Fahrenheit is %.2f degrees Celsius" %(degF, f2c(degF)))
