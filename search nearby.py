# Defined a class node with attributes data and its left and right child along with an associated structure
import copy
class Node:
    def __init__(self,data,left,right):
        self._data=data
        self._left=left
        self._right=right
        self._parent=None
        self._assoc=None
class PointDatabase():
    def __init__(self,pointlist):
        def y_sort(pointlist):     # Given a sorted binary list(either wrt x or wrt y)...constructs a balnced binary search tree
                                   # Partitions the list into two almost equal halves and assigns the root as the central data of the list
                                   #  and its left child as the elements to the left of the central data and its right child as the elements to the right of the central data
            total_nums = len(pointlist)
            if not total_nums:     
                return None
            # print(pointlist)
            elif len(pointlist)==1:
                n=Node(pointlist[0],None,None)
                return n
            elif len(pointlist)==2:
                mid_node = (len(pointlist) // 2)-1
                p= Node(pointlist[mid_node],Node(pointlist[0],None,None),Node(pointlist[1],None,None))
            else:
                mid_node = (len(pointlist) // 2)-1
                p= Node(pointlist[mid_node],y_sort(pointlist[:mid_node+1]), y_sort(pointlist[mid_node+1:]))
            return p
        
            
        def sortedArrayToBST(pointlist,lis): #This function constructs the binary search tree from a given sorted list with repect to x coordinate and assigns a associated structure(which is a binary search tree with respect to y coordinate) to every node
                                         #Associated structure of every node contains elements rooted at that particular node   
            total_nums = len(pointlist)
            new_node=y_sort(lis)
            if not total_nums:
                return None
            elif len(pointlist)==1:
                n=Node(pointlist[0],None,None)
                n._assoc=n
                return n
            elif len(pointlist)==2:
                mid_node = (total_nums // 2) -1
                p= Node(pointlist[mid_node],Node(pointlist[0],None,None), Node(pointlist[1],None,None))
                p._assoc=new_node
            else:
                mid_node = (total_nums // 2)-1
                copy_list=copy.deepcopy(lis)
                left_list,right_list=[],[]
                for i in copy_list:
                    if i[0]<=pointlist[mid_node][0]:
                        left_list.append(i)
                    else:
                        right_list.append(i)
                p= Node(pointlist[mid_node],sortedArrayToBST(pointlist[:mid_node+1],left_list), sortedArrayToBST(pointlist[mid_node + 1 :],right_list))
                p._assoc=new_node
            return p
        pointlist.sort()
        self.struc=sortedArrayToBST(pointlist,sorted(pointlist,key=lambda x:x[1]))
    def search1(self,root,x1,e):   #This function gives the upper bound for a given value.
        if root==None:
            return None
        elif  root._left==None and root._right==None:
            return root
        elif root._data[e]>=x1:
            return self.search1(root._left,x1,e)
        elif root._data[e]<x1:
            if root._right._left==None and root._right._right==None:
                if root._right._data[e]<=x1:
                    return self.search1(root._right,x1,e)
                else:
                    return self.search1(root._left,x1,e)
            else:
                return self.search1(root._right,x1,e)
    def search2(self,root,x1,e):
        if root==None:
            return None
        elif  root._left==None and root._right==None:
            return root
        elif root._data[e]>x1:
            if root._left._left==None and root._left._right==None:
                if root._left._data[e]>=x1:
                    return self.search2(root._left,x1,e)
                else:
                    return self.search2(root._right,x1,e)
            else:
                return self.search2(root._left,x1,e)
        elif root._data[e]<=x1:
            return self.search2(root._right,x1,e)
    def lca(self,root, n1, n2,e1):

        # Base Case
        if root is None:
            return None
    
        # If both n1 and n2 are smaller than root, then LCA
        # lies in left
        elif(root._data[e1] > n1._data[e1] and root._data[e1] > n2._data[e1]):
            return self.lca(root._left, n1, n2,e1)
    
        # If both n1 and n2 are greater than root, then LCA
        # lies in right
        elif(root._data[e1] < n1._data[e1] and root._data[e1] < n2._data[e1]):
            return self.lca(root._right, n1, n2,e1)
    
        return root
    def printLeafNodes(self,root,l,q,d):
        # print(l)
        if (root):
            if (not root._left and not root._right):
                if q[0]-d<=root._data[0]<=q[0]+d and q[1]-d<=root._data[1]<=q[1]+d:
                        l.append(root._data)
                # print(root._data,end = " ")
                # l.append(root._data)
            
            if root._left:
                self.printLeafNodes(root._left,l,q,d)
            if root._right:
                self.printLeafNodes(root._right,l,q,d)
        return l
    def one_d_search(self,root,q,d,ans):
        y1=q[1]-d
        y2=q[1]+d
        # print(root._data)
        r1=self.search2(root,y1,1)
        r2=self.search1(root,y2,1)
        # print(r1._data)
        # print(r2._data)
        if r1!=None and r2!=None:
            v_split=self.lca(root,r1,r2,1)
            if v_split is not None:
                
                if v_split._left==None and v_split._right==None:
                    if q[0]-d<=v_split._data[0]<=q[0]+d and y1<=v_split._data[1]<=y2:
                        # print(v_split._data)
                        ans.append(v_split._data)
                else:
                    v=v_split._left
                    if v!=None:
                        while v._left!=None and v._right!=None:
                            if y1<v._data[1]:
                                ans=self.printLeafNodes(v._right,ans,q,d)
                                v=v._left
                            else:
                                v=v._right
                        if q[0]-d<=v._data[0]<=q[0]+d and y1<=v._data[1]<=y2:
                            ans.append(v._data)
                # if v_split._left==None and v_split._right==None:
                #     if q[0]-d<=v_split._data[0]<=q[0]+d and y1<=v_split._data[1]<=y2:
                #         ans.append(v_split._data)
                # else:
                    v=v_split._right
                    if v!=None:
                        while v._left!=None and v._right!=None:
                            if y2>=v._data[1]:
                                ans=self.printLeafNodes(v._left,ans,q,d)
                                v=v._right
                            else:
                                v=v._left
                        if q[0]-d<=v._data[0]<=q[0]+d and y1<=v._data[1]<=y2:
                            ans.append(v._data)
        # print(ans,'oned')                
        return ans
    def two_d_search(self,root,q,d,ans):
        x1=q[0]-d
        x2=q[0]+d
        r1=self.search2(root,x1,0)
        r2=self.search1(root,x2,0)
        # print(x1)
        # print(x2)
        # print(r1._data)
        # print(r2._data)
        v_split=self.lca(root,r1,r2,0)
        # print(v_split._data)
        if v_split!=None:
            if v_split._left==None and v_split._right==None:
                if q[1]-d<=v_split._data[1]<=q[1]+d and x1<=v_split._data[0]<=x2:
                    ans.append(v_split._data)
            else:
                v=v_split._left
                # if v!=None:
                while v._left!=None and v._right!=None:
                    if x1<=v._data[0]:
                        # print(v._right._data)
                        if v._right._left==None and v._right._right==None:
                            if q[1]-d<=v._right._data[1]<=q[1]+d and x1<=v._right._data[0]<=x2:
                                ans.append(v._right._data)
                        ans=self.one_d_search(v._right._assoc,q,d,ans)
                        # print(ans,'1')
                        v=v._left
                        # print('no',v._data)
                    else:
                        v=v._right
                if q[1]-d<=v._data[1]<=q[1]+d and x1<=v._data[0]<=x2:
                    ans.append(v._data)
                v=v_split._right
                # if v!=None:
                while v._left!=None and v._right!=None:
                    if x2>=v._data[0]:
                        if v._left._left==None and v._left._right==None:
                            if q[1]-d<=v._left._data[1]<=q[1]+d and x1<=v._left._data[0]<=x2:
                                ans.append(v._left._data)
                        ans=self.one_d_search(v._left._assoc,q,d,ans)
                        # print(ans,'2')
                        v=v._right
                    else:
                        v=v._left
                if q[1]-d<=v._data[1]<=q[1]+d and x1<=v._data[0]<=x2:
                    ans.append(v._data)
            
        return list(set(ans))
    def searchNearby(self,q,d):
        return self.two_d_search(self.struc,q,d,[])


            

        


        # --------------------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------------------
         
    def height(self,node):
        if node is None:
            return 0
        else:
            # Compute the height of each subtree
            lheight = self.height(node._left)
            rheight = self.height(node._right)
    
            # Use the larger one
            if lheight > rheight:
                return lheight+1
            else:
                return rheight+1
    def printCurrentLevel(self,root, level):
        if root is None:
            return
        if level == 1:
            print(root._data, end="")
        elif level > 1:
            self.printCurrentLevel(root._left, level-1)
            self.printCurrentLevel(root._right, level-1)
    def printLevelOrder(self,root):
        h = self.height(root)
        for i in range(1, h+1):
            self.printCurrentLevel(root, i)


# Print nodes at a current level

# ==========================================================================================================================================
# ==========================================================================================================================================
# ===================================================================================================================================        
    # def inorder(self,root):
    #     if root == None:
    #         return None
    #     else:
    #         print(root._data,end='')
    #         self.inorder(root._left)
    #         self.inorder(root._right)
        # def preorder(root):
        #     if root == None:
        #         return None
        #     else:
                
        #         preorder(root._left)
        #         print(root._data,end='')
        #         preorder(root._right)
        
        # self.rep=sortedArrayToBST(pointlist)
        # self.rep=sortedArrayToBST(pointlist)
        # print(self.rep._left._right._data)
        # print(inorder(self.rep._left._right._assoc))
        # print(printLevelOrder(self.rep._left._right._assoc))
        # print(inorder(self.rep._left._assoc))
        # print(printLevelOrder(self.rep._left._assoc))
        # print(printLeafNodes(self.rep._left._assoc,[]))
        # print(inorder(self.rep))
        # print(preorder(self.rep))
        # print(printLeafNodes(self.rep,[]))
        # print(two_d_search(self.rep,(4,8),0.25,[]))
        # print(one_d_search(self.rep._left._assoc,(5,5),1,[]))
        # print(search(self.rep._assoc,6,1)._data)
        # print(printLevelOrder(self.rep))
    # def searchNearby(self,q,d):


# pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)])
# pointDbObject=PointDatabase([(21, 24), (9, 8), (13, 38), (17, 45), (35, 23), (5, 47), (46, 5), (38, 2), (4, 20), (22, 50), (40, 28), (43, 26), (31, 22), (8, 35), (27, 25)])
# pointDbObject=PointDatabase([(38, 26), (43, 24), (5, 25), (30, 2), (29, 7), (37, 16), (51, 15), (40, 23), (23, 20), (8, 49), (34, 45), (42, 12), (32, 39), (17, 19), (12, 4)])
# pointDbObject=PointDatabase([(32, 72), (68, 52), (10, 59), (71, 85), (99, 96), (86, 7), (82, 65), (29, 50), (96, 49), (52, 94), (56, 93), (88, 78), (75, 98), (26, 56), (34, 26), (43, 55), (70, 80), (22, 30), (60, 47), (39, 70)])
# pointDbObject = PointDatabase([(2,4)])
# print(pointDbObject.printLevelOrder(pointDbObject.struc._right._right._assoc))
# print(pointDbObject.searchNearby((12,14),6.4))
# print(pointDbObject.searchNearby((20,40),37.9))
# print(pointDbObject.searchNearby((18,69),69.5)) 
# print(pointDbObject.searchNearby((10,6),40.0))
