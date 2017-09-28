'''
    ============================================================================
    Module: RuleSet
    ============================================================================
    This module implements the API for the coherence checking and Options
    toggling mechanism.
'''

# coded by: Animesh Karnewar

class RuleSet:
    '''
        The Data type for holding the rules defined for certain options to be toggled
    '''


    def __init__(self):
        '''
            constructor of the class. Creates an empty RuleSet
        '''
        # initialize all that data structures to emty sets
        self.__deps = set()
        self.__confs = set()
        self.__symbols = set()
        # the preceding underscore means that all the members are private


    def addDep(self, dest, source):
        '''
            method to add a dependency relation to the RuleSet
            @param
            dest => the symbol at the receiving end of dependency
            source => the symbol at the source of dependency
        '''
        # the implementation logic is pretty simple
        dependency = (dest, source) # the tuple representing the dependency relationship
        self.__deps.add(dependency)

        # add the two new symbols to the set.
        self.__symbols.add(dest); self.__symbols.add(source)
        # set only contains unique entries. So, repeating entries will not occur


    def addConflict(self, sym1, sym2):
        '''
            method to add the mutual exclusion (conflict) relation to the RuleSet
            @param
            sym1 => first symbol
            sym2 => second symbol
        '''
        # implementation is again quite lucid
        conflict = (sym1, sym2) # reverse is also same
        # since 'a and b' mutually exclusive also means 'b and a' are too.
        self.__confs.add(conflict)

        # add the two symbols to the symbol set
        self.__symbols.add(sym1); self.__symbols.add(sym2)


    def isCoherent(self):
        '''
            method to check if the Rules in the RuleSet are coherent
            @return => bool status of coherence
        '''
        pass


    # ==========================================================================
    # Following are some of the utility methods. They are not necessarily used
    # for any logical operations
    # ==========================================================================

    # Recursive method
    def areDependent(self, dest, source):
        '''
            Recursive method to check if the two symbols directly or indirectly
            depend on each other.
            @Param
            dest => receiving end of potential dependency
            source => source of potential dependency
        '''
        if((dest, source) in self.__deps):
            ''' Base case '''
            return True

        else:
            ''' Recursion case '''
            # extract lists of elements that are directly depended upon by dest
            # and those that directly depend on source
            check_dst = []; check_src = [] # initialy empty lists
            for dependency in self.__deps:
                if(dependency[0] == dest):
                    check_dst.append(dependency[1])
                if(dependency[1] == source):
                    check_src.append(dependency[0])

            # now check if there is any symbol in check_dst that also appears in check_src
            dependence_found = False
            for sym in check_dst:
                if(sym in check_src):
                    dependence_found = True # dependence has been located
                    break;

            if(dependence_found):
                return True # if we have located a dependence, then return true

            else:
                # generate full cross join of check_dst and check_src.
                # if len(check_dst) = 3 and len(check_src) = 4
                # there will be in all 3 * 4 = 12 elements in the cross join
                crs_join = [] # initialize to empty list
                for sym1 in check_dst:
                    for sym2 in check_src:
                        crs_join.append((sym1, sym2))

                # now perform the checks recursively
                return reduce(lambda x, y: x or y,
                            map(lambda x: self.areDependent(x[0], x[1]), crs_join), False)

    def getDependencies(self):
        '''
            method to return the dependencies currently in the RuleSet
            @return => the dependencies
        '''
        return self.__deps.copy() # be careful not to return the private copy

    def getConflicts(self):
        '''
            method to return the conflicts currently in the RuleSet
            @return => the conflicts
        '''
        return self.__confs.copy()

    def getSymbols(self):
        '''
            method to return the Symbols currently in the RuleSet
            @return => the unique symbols in use
        '''
        return self.__symbols.copy()


if(__name__ == "__main__"):
    ''' Api usage script and naive testing '''

    print "\n\t\t!!! Welcome to the api usage script !!!\n"

    # create a new RuleSet object
    rs = RuleSet()

    # add a few dependencies
    rs.addDep("a", "b")
    rs.addDep("c", "d")

    # print and check the currently present
    print "Currently present dependencies: " + str(rs.getDependencies()) + "\n\n"

    # add some conflicts
    rs.addConflict("a", "b")
    rs.addConflict("e", "f")

    # print and check the currently present conflicts
    print "Currently present conflicts: " + str(rs.getConflicts()) + "\n\n"

    ts = RuleSet()
    ts.addDep("a", "b")
    ts.addDep("b", "c")
    ts.addDep("c", "d")
    ts.addDep("d", "e")
    print ts.getDependencies()
    print ts.areDependent("deman", "londa")
