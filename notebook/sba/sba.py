import pandas as pd
from collections import defaultdict
import numpy as np
import logging

class TreeNode:

    def __init__(self):
        self.id = ()
        self.children = {}

        self.aggregated = None
        self.data_at_leaf = None

    def get_name(self):
        return self.id[-1]

    def __getitem__(self, key):
        return self.children[key]


class TreeBase:

    def __init__(self, full_id_keys, df):

        self.full_id_keys = full_id_keys

        self.df = df

        self.root_node = TreeNode()
        self._insert_node(self.root_node, df)

        #df_rw = pd.read_csv('./configs/risk_weight_1.csv')
        #kw_rw = defaultdict(lambda: defaultdict(list))
        #for r in df_rw.itertuples():
        #    kw_rw[r[1]]
        #self.df_ext = df.copy()

        pass


    def _insert_node(self, node: TreeNode, df_node: pd.DataFrame):
    
        node_id = node.id
        node_id_len = len(node_id)
        b_top_node = node_id_len == 0

        # if the node is a leaf node
        if node_id_len == len(self.full_id_keys):
            node.data_at_leaf = df_node.copy()
            return


        # if the node is not a leaf node
        by_cols = self.full_id_keys[:(node_id_len+1)]
        grpby_df_node = df_node.groupby(by_cols)
        for subnode_id in grpby_df_node.groups:
            
            # The groupby makes keys in terms of tuples. 
            # If at the top node, it does not create a tuple. 
            # To make a tuple with a single entry, ',' should be appended
            subnode_id_tuple = (subnode_id, ) if b_top_node else subnode_id
            
            df_subnode = grpby_df_node.get_group(subnode_id)
            subnode = TreeNode()
            subnode.id = subnode_id_tuple
            node.children[subnode.get_name()] = subnode

            self._insert_node(subnode, df_subnode)

        # remove
        grpby_df_node = None

    def get_node(self, node_id, default_key):
        
        curr_node = self.root_node
        for name in node_id:
            if name in curr_node.children:
                curr_node = curr_node.children[name]
            else:
                curr_node = curr_node.children[default_key]

        return curr_node

    def _aggregate_leaf_node(self, node_attrs, df_node):
        raise NotImplementedError("not implemented yet")
        
    def _aggregate_nonleaf_node(self, node_attrs, kw_res_subnodes):
        raise NotImplementedError("not implemented yet")





    
if __name__ == '__main__':

    nA = 4
    nR = 500
    df = pd.DataFrame(index=range(nR), columns=['A'+str(i) for i in range(nA)] + ['V'], 
                    data=np.random.randint(0, 10, size=[nR, nA+1]))

    tb = TreeBase(['A0','A1','A2'], df)
    node = tb.get_node([1,2,3], 0)

    pass


        #     logging.info('aggregation at ' + str(node_id))

        # node_id_len = len(node_id)
        # b_top_node = node_id_len == 0

        # # if the node is a leaf node
        # if node_id_len == len(self.full_id_keys):
        #     res_node = self._aggregate_leaf_node(node_id, df_node)
        #     node.children[node_name] = df_node
        #     node.data = res_node
        
        # # if the node is not a leaf node
        # by_cols = self.full_id_keys[:(node_id_len+1)]
        # grpby_df_node = df_node.groupby(by_cols)
        # kw_res_subnodes = {}
        # for subnode_attrs in grpby_df_node.groups:
            
        #     # The groupby makes keys in terms of tuples. 
        #     # If at the top node, it does not create a tuple. 
        #     # To make a tuple with a single entry, ',' should be appended
        #     subnode_attrs_tuple = (subnode_attrs, ) if b_top_node else subnode_attrs
            
        #     df_subnode = grpby_df_node.get_group(subnode_attrs)
        #     res_subnode = self._create_node(
        #         subnode_attrs_tuple, df_subnode)

        #     kw_res_subnodes[subnode_attrs_tuple] = res_subnode

        # res_node = self._aggregate_nonleaf_node(node_id, kw_res_subnodes)

        # return res_node