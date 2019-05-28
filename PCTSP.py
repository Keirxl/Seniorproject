# "N" is the number of 'cities'
# The Edges are a list for the constraints to draw from
# The matrix is a nest list of the travel times in minutes from 'city' to 'city' the last value in each list is the time expected to be spent there
#USE A BLANK TEXT FILE CALLED forlp.txt to write the LPsolve text to.
n=15
edges = []
for i in range(1,n+1):
	if i>9:
		edges.append(str(i))
	else:
		edges.append("0"+str(i))
matrix =[[0,8,9,20,30,8,14,15,17,8,12,9,8,9,16,120],[8,0,4,25,39,19,22,15,21,9,11,6,8,14,22,60],[9,4,0,25,39,19,22,15,21,9,11,6,8,14,22,60],[20,25,25,0,17,6,7,31,38,13,31,29,12,20,43,180],[30,39,39,17,0,21,20,40,52,28,43,37,28,36,50,180],[8,19,19,6,21,0,10,25,27,9,32,28,13,10,40,180],[14,22,22,7,20,10,0,28,30,12,32,22,12,12,44,60],[15,15,15,31,40,25,28,0,8,15,20,14,14,24,27,60],[17,21,21,38,52,27,30,8,0,22,27,15,24,28,34,120],[8,9,9,13,28,9,12,15,22,0,14,15,1,11,29,60],[12,11,11,31,43,32,32,20,27,14,0,10,13,21,33,60],[9,6,6,29,37,28,22,14,15,15,10,0,13,22,25,60],[8,8,8,12,28,13,12,14,24,1,13,13,0,11,29,120],[9,14,14,20,36,10,12,24,28,11,21,22,11,0,42,120],[17,22,22,43,50,40,44,27,34,29,33,25,29,42,0,180]]
prizes=["0"]
#User Starts here
		
		
print ("On a scale of 1 to 10 please rate the following attractions based on how much you would like to visit them, and then input about how long (in minutes) you would like to spend on this tour.")
LibBell = input("The Liberty Bell: ")
prizes.append(LibBell)
ConCenter = input("The Constitution Center: ")
prizes.append(ConCenter)
Art = input("The Philadelphia Museum of Art: ")
prizes.append(Art)
Zoo = input("The Philadelphia Zoo: ")
prizes.append(Zoo)
FranklinINST = input("The Franklin Institute: ")
prizes.append(FranklinINST)
Rodin = input("The Rodin Museum: ")
prizes.append(Rodin)
MagicGard = input("The Magic Gardens: ")
prizes.append(MagicGard)
ItalianMRKT = input("The Italian Market: ")
prizes.append(ItalianMRKT)
OneLiberty = input("One Liberty Observation Deck: ")
prizes.append(OneLiberty)
ElfrethsAlley = input("Elfreth's Alley: ")
prizes.append(ElfrethsAlley)
FranklinSQR = input("Franklin Square: ")
prizes.append(FranklinSQR)
Shops = input("The Shops at Liberty Place: ")
prizes.append(Shops)
Mutter = input("The Mutter Museum: ")
prizes.append(Mutter)
Aqua = input ("The Camden Aquarium: ")
prizes.append(Aqua)
TimeSpent = input("How long would you like to tour?")

#This part lets the user know how to read the results in LpSolve
userkey = open('forlp.txt','a')
userkey.write("/*The Way to read the result is to go to the objective tab and use the following to determine what cities to visit. It is a binary system so a 1 means that attraction is visited and a 0 means it is not used. The y's are attractions and the x's are the routes between the attractions. For instance x0102 is the route from attraction one to attraction two*/")
userkey.write("/*y01 = The Convention Center(Home)\n y02 = The Liberty Bell\n y03 = The Constitution Center\n y04 = The Art Museum\n y05 = The Zoo\n y06 = The Franklin Institute\n y07 = The Rodin Museum\n y08 = The Magic Gardens\n y09 = The Italian Market\n y10 = One Liberty Observation Deck\n y11 = Elfreth's Alley\n y12 = Franklin Square\n y13 = The Shops at Liberty Place\n y14 = The Mutter Museum\n y15 = The Camden Aquarium*/\n")
userkey.close()

#This writes the Objective Function
objfunc = open('forlp.txt','a')
objfunc.write("/* This is the Objective Function */")
objfunc.write("Max: ")
for i in range(0,n):
	objfunc.write("+"+prizes[i]+"y"+edges[i])
objfunc.write(";\n\n")
objfunc.close()

#This Part creates the node degree two constraint
st_one = open("forlp.txt","a")
st_one.write("/* These are the node degree two constraints */")
edgelist = []
for i in range(0,n):
	for j in range(0,n):
		if i>j:
			st_one.write(("x"+edges[j]+edges[i]+"+"))
		elif i<j:
			st_one.write(("x"+edges[i]+edges[j]+"+"))
	st_one.write("0=2y"+edges[i]+";\n")
st_one.close()

#this part makes the time <10hours constraint
st_two = open('forlp.txt','a')
for i in range(0,n):
	for j in range(i+1,n):
		st_two.write(str(matrix[i][j]))
		st_two.write(("x"+edges[i]+edges[j]+"+")) 
for i in range(0,n):
	st_two.write(str(matrix[i][n])+"y"+edges[i]+"+")
st_two.write("0 <"+TimeSpent+";\n")#ten hours in minutes
st_two.close()



#These are the flow Constraints 
st_five = open('forlp.txt','a')
st_five.write("/* These are the Flow Constraints */")
for k in range(2,n+1):
	for i in range(0,n):
		for j in range(i+1,n):
			st_five.write("F"+str(k)+edges[i]+edges[j])
			st_five.write("+"+"F"+str(k)+edges[j]+edges[i])
			st_five.write("<=x"+edges[i]+edges[j]+"; \n")
st_five.close()
st_six = open('forlp.txt','a')
for k in range(2,n+1):
	for j in range(1,n):
		st_six.write("F"+str(k)+"01"+edges[j]+"-")
		st_six.write("F"+str(k)+edges[j]+"01"+"+")
	st_six.write("0"+"=2y"+edges[k-1]+"; \n")
st_six.close()
st_seven = open('forlp.txt','a')
for k in range(2,n+1):
	for i in range(1,n):
		if i+1 != k:
			for j in range(0,n):
				if i != j:
					st_seven.write("F"+str(k)+edges[i]+edges[j]+"-")
					st_seven.write("F"+str(k)+edges[j]+edges[i]+"+")
			st_seven.write("0"+"=0; \n")
st_seven.close()
st_eight = open('forlp.txt','a')
for k in range(2,n):
	for i in range(0,n):
		for j in range(0,n):
			if i != j:
				st_eight.write("0<="+"F"+str(k)+edges[i]+edges[j]+"<=1; \n")
st_eight.close()

#home must be visited constraint and binaries
st_three = open('forlp.txt','a')
st_three.write("/* These are the binary constraints and the constraint that the Home must be visited */")
st_three.write("y01 = 1;\n")
st_three.write("bin ")
for i in range(0,n):
	for j in range(0,n):
		if i>j:
			st_three.write(("x"+edges[j]+edges[i]+","))
		elif i<j:
			st_three.write(("x"+edges[i]+edges[j]+","))
for i in range(0,n):
	if i == n-1:
		st_three.write("y"+edges[i]+"; \n")
	else:
		st_three.write("y"+edges[i]+",")
st_three.close()








