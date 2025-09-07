# print("Hello world!")

# name = "kumaresan"
# result = "u" not in name

# print(result)

# fruits = ["mango", "apple", "orange"]
# print(fruits)

# fruits.append("grapes")
# print(fruits)

# sampleDictionary = {"myname":"kumaresan", "wife":"Manisha"}
# sampleDictionary.update({"sister":"Mari"})
# print(sampleDictionary)

# money = int(input("How much money you have?"))

# if(money >= 50):
#     order = str(input("We have pongal, vada, idli, tea. what do you want? "))
#     match order:
#         case "pongal":
#             print("Ordered pongal")
#         case "vada":
#             print("Ordered vada")
#         case "idli":
#             print("Ordered idli")
#         case "tea":
#             print("Ordered tea")
#         case _:
#             print("Sorry, We don't have " + order)


#For loop example

# fruits = ["apple", "orange", "banana"]

# for i in fruits:
#     print(i)

#while loop exmple

# i = 1

# while i<=10:
#     print(i)
#     i += 1

#Functions in python example.

# a = 5
# b = 7

# def add(a, b):
#     return a + b

# c = add(a, b)
# print(c)

#try except block example.
# try:
#     a = 5/0
# except Exception as e:
#     print(e)
# else:
#     print("if exception doesn't occured inside try block, this else part will be execuated.")
# finally:
#     print("This block will be executed always whether the exception occured or not")

#File handling example
# file = open("TestFile.txt", "r") #loaded the file in the variable file. have to give file location and purpose(ex: r for read, w for write, a for append the content)
# content = file.read()
# print(content)

# file = open("TestFile.txt", "w") #delete the old content and add this new content.
# content = file.write("new content")
# file.close()

# file = open("TestFile.txt", "a") #Append the content with already existing content.
# content = file.write("\nappended content")
# file.close()

#simplified code to handle file
# with open("TestFile.txt", "r") as file:
#     content = file.read()
#     print(content)
#     file.close()

#Example for importing package from another folder and use method from that.
    #Create the folder named TestPackageFolder
    #Created the file __ini__.py. if you wanna use the folder as a package, you should create this file under the folder.
    #Create the python file and add all your functions to use it in other python files.
# import TestPackageFolder.test_package as add

# c = add.testAddMethod(2, 3)
# print(c)