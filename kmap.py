# file by joshua

class Minterm:
    def __init__(self, key): # input needs to be an integer
        self.key = int(key)
        self.bcd = None
        self.split = None
        self.selected = False
        self.isIncluded = False
    
    def __str__(self):
        res = "Minterm Node is: " + str(self.key) + ", BCD: " + str(self.bcd)
        return res
        
    def __getitem__(self, idx):
        return self.split[idx]
    
    def assign(self, assignment): # input needs to be str
        self.bcd = assignment
        res = [int(i) for i in assignment] #split
        self.split = res
        
    def select(self):
        self.selected = True
    
class Group:
    def __init__(self, key): # input key is str
        self.members = []
        self.tier = 0
        self.key = str(key)
        self.split = [i for i in key]
        self.dominated = False
    
    def addMinterm(self, item):
        self.members.append(item)
        self.tier += 1
        
    def __str__(self):
        print("Group:", str(self.key))
        print("Members:")
        print([str(i.key) for i in self.members])
        return ""
    
    def __getitem__(self,x):
        return self.split[x]
    
    def __contains__(self,n):
        return n in self.members
    
    
class kmap:
    def __init__(self, variables, minterms):
        self.variables = int(variables)
        self.minterms = minterms # this is a list
        self.nodes = [] # minterm nodes
        self.groups = [] # group nodes
        self.bcd = {}
        
        if variables not in [3,4]:
            raise ValueError("Machine only limited to 3 or 4 variables!")
        for minterm in self.minterms:
            if self.variables == 3:
                if minterm > 7:
                    raise ValueError("3 Variables: Choose from 0-7 minterms values only!")
            elif self.variables == 4:
                if minterm > 15:
                    raise ValueError("4 Variables: Choose from 0-15 minterms values only!")
            
        bcd_4 = {
            0:"0000", 1:"0001", 2:"0010",
            3:"0011", 4:"0100", 5:"0101",
            6:"0110" , 7:"0111", 8:"1000",
            9:"1001", 10:"1010", 11:"1011",
            12:"1100", 13:"1101", 14:"1110",
            15:"1111"
        }
        bcd_3 = {
            0:"000", 1:"001", 2:"010",
            3:"011", 4:"100", 5:"101",
            6:"110" , 7:"111"
        }
        
        # assign proper bcd values
        if self.variables == 3:
            self.bcd = bcd_3
        elif self.variables == 4:
            self.bcd = bcd_4
            
        # convert int minterms to nodes and set primary group
        for minterm in self.minterms: # list
            node = Minterm(minterm) #int is being inserted as arg of Minterm
            node.assign(self.bcd[node.key])# assign appropriate BDC
            self.nodes.append(node) # append to dictionary
        
        self.solve()
        
    def p3(self):
        print("=========   3 Variable K-Map   =========")
        print("")
        r1 = [[0],[0],[0],[0]]
        r2 = [[0],[0],[0],[0]]
        head = "\BC  [00] [01] [11] [10] "
        
        for i in self.minterms:
            if i == 0:
                r1[0] = [1]
            if i == 1:
                r1[1] = [1]
            if i == 2:
                r1[3] = [1]
            if i == 3:
                r1[2] = [1]
            if i == 4:
                r2[0] = [1]
            if i == 5:
                r2[1] = [1]
            if i == 6:
                r2[3] = [1]
            if i == 7:
                r2[2] = [1]
        
        print(head)
        print("A 0|", str(r1))
        print("  1|", str(r2))
        print("")
        print("========================================")
    
    def p4(self):
        print("=========   4 Variable K-Map   =========")
        print("")
        r1 = [[0],[0],[0],[0]]
        r2 = [[0],[0],[0],[0]]
        r3 = [[0],[0],[0],[0]]
        r4 = [[0],[0],[0],[0]]
        
        for i in self.minterms:
            if i == 0:
                r1[0] = [1]
            if i == 1:
                r1[1] = [1]
            if i == 2:
                r1[3] = [1]
            if i == 3:
                r1[2] = [1]
                
            if i == 4:
                r2[0] = [1]
            if i == 5:
                r2[1] = [1]
            if i == 6:
                r2[3] = [1]
            if i == 7:
                r2[2] = [1]
                
            if i == 8:
                r4[0] = [1]
            if i == 9:
                r4[1] = [1]
            if i == 10:
                r4[3] = [1]
            if i == 11:
                r4[2] = [1]
                
            if i == 12:
                r3[0] = [1]
            if i == 13:
                r3[1] = [1]
            if i == 14:
                r3[3] = [1]
            if i == 15:
                r3[2] = [1]
                
        head = "  \CD  [00] [01] [11] [10] "
        print(head)
        print("AB 00|", str(r1))
        print("   01|", str(r2))
        print("   11|", str(r3))
        print("   10|", str(r4))
        print("")
        print("========================================")

    def show_minimal(self):
        res = "Minimal Sum of Products: [ "
        if len(self.groups) != 1 and len(self.groups) != 2:
            for indx in range(len(self.groups)-1):
                res += str(self.groups[indx].key) + " + "
            res += (str(self.groups[-1].key) +  " ]")
            print(res)
        elif len(self.groups) == 1:
            res += (str(self.groups[-1].key) +  " ]")
            print(res)
        elif len(self.groups) == 2:
            res += (str(self.groups[0].key) + " + " + str(self.groups[1].key) + " ]")
            print(res)
    
    def solve(self):
        # solve according to number of variables
        if self.variables == 3:
            self.sol3()
            self.p3()
            print("Minterms are:")
            print(sorted(self.minterms))
            self.show_minimal()
        elif self.variables == 4:
            self.sol4()
            self.p4()
            print("Minterms are:")
            print(sorted(self.minterms))
            self.show_minimal()
        

    def sol3(self):
        self.groups = []
        groupdict = {
            "0**":Group("0**"),"1**": Group("1**"),"*0*": Group("*0*"),
            "*1*": Group("*1*"),"**0": Group("**0"),"**1": Group("**1"),
            "*00":Group("*00"),"*01":Group("*01"),"*11":Group("*11"),
            "*10":Group("*10"),"00*":Group("00*"),"01*":Group("01*"),
            "11*":Group("11*"),"10*":Group("10*"),"0*0":Group("0*0"),
            "0*1":Group("0*1"),"1*1":Group("1*1"),"1*0":Group("1*0")
            }
        
        for minterm in self.nodes:
            a = minterm[0]
            b = minterm[1]
            c = minterm[2]
            v1k_a = str(a) + "**"
            v1k_b = "*" + str(b) + "*"
            v1k_c = "**" + str(c)
            v2k_ab = str(a) + str(b) + "*"
            v2k_ac = str(a) + "*" + str(c)
            v2k_bc = "*" + str(b) + str(c)
            v1 = [v1k_a, v1k_b,v1k_c]
            v2 = [v2k_ab, v2k_ac, v2k_bc]
            
            for v1_str in v1:
                groupdict[v1_str].addMinterm(minterm)
            for v2_str in v2:
                groupdict[v2_str].addMinterm(minterm)
            
        hold = []
        #  find dominant 1 var, 4 max mem
        for g_key in groupdict:
            if groupdict[g_key].split.count("*") == 2: # 1 var
                if groupdict[g_key].tier == 4: # full cap
                    self.groups.append(groupdict[g_key])
            elif groupdict[g_key].split.count("*") == 1: # 2 var
                if groupdict[g_key].tier not in [0,1]:
                    hold.append(groupdict[g_key])
        
        # see if 2 vars are dominated:
        limit_list = ["0**", "1**","*0*", "*1*","**0", "**1"]
        for limit in limit_list:
            if groupdict[limit] in self.groups:
                for code in groupdict[limit].split:
                    if code != "*":
                        ind = groupdict[limit].split.index(code)
                        for i in hold:
                            if i.split[ind] != groupdict[limit].split[ind]:
                                self.groups.append(i)
                            if i.split[ind] == groupdict[limit].split[ind]:
                                i.dominated = True

        # add non dominated groups
        for token in hold:
            if not token.dominated and token not in self.groups:
                self.groups.append(token)
            
        # added minterms --> selected
        for added in self.groups:
            for terms in added.members:
                terms.selected = True
        for minterm in self.nodes:
            if not minterm.selected:
                temp = Group(minterm.bcd)
                temp.addMinterm(minterm)
                self.groups.append(temp)
                minterm.selected = True

        # simplify by identifying essential primes
        essentials = []
        to_remove = []
        for i in self.groups:
            current = i
            if current.tier != 1:
                all_others = []
                for part in self.groups:
                    if part != current and part.tier != 1:
                        for term in part.members:
                            all_others.append(term)
                for xxx in all_others:
                    if not set(current.members).issubset(all_others) and current not in essentials:
                        essentials.append(current)
                    elif set(current.members).issubset(all_others):
                        if current not in to_remove:
                            to_remove.append(current)
        
        for i in to_remove:
            self.groups.remove(i)
            
        for clu in self.groups:
            for mem in clu.members:
                mem.isIncluded = True

        for g in self.nodes:
            if not g.isIncluded:
                for xxx in to_remove:
                    if g in xxx.members and xxx not in self.groups and not g.isIncluded:
                        self.groups.append(xxx)
                        for qq in xxx.members:
                            qq.isIncluded = True
                    if g.isIncluded:
                        break

         # check if 1 or 0
        if len(self.minterms) == 8: # full set
            self.groups = []
            temp = Group("1")
            for i in self.nodes:
                temp.addMinterm(temp)
            self.groups.append(temp)
        if len(self.minterms) == 0:
            self.groups = []
            temp = Group("0")
            self.groups.append(temp)
            
    def sol4(self):
        self.groups = []
        gdict = {
            "0***": Group("0***"), "1***": Group("1***"), "*0**": Group("*0**"), "*1**": Group("*1**"),
            "**0*": Group("**0*"), "**1*": Group("**1*"),"***0": Group("***0"), "***1": Group("***1"),
            "00**": Group("00**"),"01**": Group("01**"),"11**": Group("11**"),"10**": Group("10**"),
            "**00": Group("**00"),"**01": Group("**01"),"**11": Group("**11"),"**10": Group("**10"),
            "0*0*": Group("0*0*"),"0*1*": Group("0*1*"),"1*1*": Group("1*1*"),"1*0*": Group("1*0*"),
            "0**0": Group("0**0"),"0**1": Group("0**1"),"1**1": Group("1**1"),"1**0": Group("1**0"),
            "*00*": Group("*00*"),"*01*": Group("*01*"),"*11*": Group("*11*"),"*10*": Group("*10*"),
            "*0*0": Group("*0*0"),"*0*1": Group("*0*1"),"*1*1": Group("*1*1"),"*1*0": Group("*1*0"),
            "000*": Group("000*"),"001*": Group("001*"),"010*": Group("010*"),"011*": Group("011*"),
            "100*": Group("100*"),"101*": Group("101*"),"110*": Group("110*"),"111*": Group("111*"),
            "00*0": Group("00*0"),"00*1": Group("00*1"),"01*0": Group("01*0"),"01*1": Group("01*1"),
            "10*0": Group("10*0"),"10*1": Group("10*1"),"11*0": Group("11*0"),"11*1": Group("11*1"),
            "0*00": Group("0*00"),"0*01": Group("0*01"),"0*10": Group("0*10"),"0*11": Group("0*11"),
            "1*00": Group("1*00"),"1*01": Group("1*01"),"1*10": Group("1*10"),"1*11": Group("1*11"),
            "*000": Group("*000"),"*001": Group("*001"),"*010": Group("*010"),"*011": Group("*011"),
            "*100": Group("*100"),"*101": Group("*101"),"*110": Group("*110"),"*111": Group("*111")
        }
        
        for minterm in self.nodes:
            a = minterm[0]
            b = minterm[1]
            c = minterm[2]
            d = minterm[3]
            a1k = str(a) + "***"
            b1k = "*" +  str(b) + "**"
            c1k = "**" + str(c) + "*"
            d1k = "***" + str(d)
            ab2 = str(a) + str(b) + "**"
            cd2 = "**" + str(c) + str(d)
            ac2 = str(a) + "*" + str(c) + "*"
            ad2 = str(a) + "**" + str(d)
            bc2 = "*" + str(b) + str(c) + "*"
            bd2 = "*" + str(b) + "*" + str(d)
            abc3 = str(a) + str(b) + str(c) + "*"
            abd3 = str(a) + str(b) + "*" + str(d)
            acd3 = str(a) + "*" + str(c) + str(d)
            bcd3 = "*" + str(b) + str(c) + str(d)
            v1k = [a1k,b1k,c1k,d1k]
            v2k = [ab2,cd2,ac2,ad2,bc2,bd2]
            v3k = [abc3,abd3,acd3,bcd3]
            # add to 1 var and 3 var (since same len)
            for var1_str in v1k:
                gdict[var1_str].addMinterm(minterm)
                
            # add 2 var
            for var2_str in v2k:
                gdict[var2_str].addMinterm(minterm)
                
            for var3_str in v3k:
                gdict[var3_str].addMinterm(minterm)

        hold4 = []
        # find most dominant 1 var, 8 members
        for str_4 in gdict:
            if gdict[str_4].split.count("*") == 3: # 3*'s and just 1 var:
                if gdict[str_4].tier == 8: # has to be full
                    self.groups.append(gdict[str_4])
            elif gdict[str_4].split.count("*") == 2: # 2 var
                if gdict[str_4].tier == 4:
                    hold4.append(gdict[str_4])
            elif gdict[str_4].split.count("*") == 1: # 3 var
                if gdict[str_4].tier == 2:
                    hold4.append(gdict[str_4])
            
        # find 4-max clusters and see if it is dominated, (clust is 2 var)
        limitations = [["0***","1***"],["*0**", "*1**"],["**0*", "**1*"],["***0","***1"]]
        
        for lim in ["0***","1***","*0**", "*1**","**0*", "**1*","***0","***1"]:
            if gdict[lim] in self.groups:
                for code in gdict[lim].split:
                    if code != "*":
                        ind = gdict[lim].split.index(code)
                        for i in hold4:
                            if i.split[ind] != gdict[lim].split[ind]:
                                self.groups.append(i)
                            if i.split[ind] == gdict[lim].split[ind]:
                                i.dominated == True
        

        # set domination for 3 var (2 member) group
        lim2var = ["00**","01**","11**","10**","**00","**01","**11","**10",
                   "*00*","*01*","*11*","*10*","0**0","0**1","1**1","1**0",
                   "0*0*","0*1*","1*1*","1*0*","*0*0","*0*1","*1*1","*1*0",]
        
        for lim3 in lim2var:
            if gdict[lim3] in hold4 and gdict[lim3].tier == 4:
                varind = []
                for non_ast_ind in range(len(gdict[lim3].split)):
                    if gdict[lim3].split[non_ast_ind] != "*":
                        varind.append(non_ast_ind)
                for i in hold4:
                    if i.split.count("*") == 1:
                        if i.split[varind[0]] == gdict[lim3].split[varind[0]] and i.split[varind[1]] == gdict[lim3].split[varind[1]]:
                            i.dominated = True
        
        # only add not dominated nodes
        for token in hold4:
            if not token.dominated and token not in self.groups:
                self.groups.append(token)
        
        # add self nodes
        for added in self.groups:
            for terms in added.members:
                terms.selected = True
        
        for minterm in self.nodes:
            if not minterm.selected:
                temp = Group(minterm.bcd)
                temp.addMinterm(minterm)
                self.groups.append(temp)
                minterm.selected = True
        
        # simplify by identifying essential primes
        essentials = []
        to_remove = []
        
        for i in self.groups:
            current = i
            if current.tier != 1:
                all_others = []
                for part in self.groups:
                    if part != current and part.tier != 1:
                        for term in part.members:
                            all_others.append(term)
                for xxx in all_others:
                    if not set(current.members).issubset(all_others):
                        essentials.append(current)
                    elif set(current.members).issubset(all_others):
                        if current not in to_remove:
                            to_remove.append(current)
        
        for i in to_remove:
            self.groups.remove(i)
            
        for clu in self.groups:
            for mem in clu.members:
                mem.isIncluded = True
        
        for g in self.nodes:
            if not g.isIncluded:
                for xxx in to_remove:
                    if g in xxx.members and xxx not in self.groups and not g.isIncluded:
                        self.groups.append(xxx)
                        for qq in xxx.members:
                            qq.isIncluded = True
                    if g.isIncluded:
                        break
        
        # check if 1 or 0
        if len(self.minterms) == 16: # full set
            self.groups = []
            temp = Group("1")
            for i in self.nodes:
                temp.addMinterm(temp)
            self.groups.append(temp)
        if len(self.groups) == 0:
            self.groups = []
            temp = Group("0")
            self.groups.append(temp)
