
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'DOT EQUALS FOR ID INT LBRACE LEQ LPAREN NUM PLUS RBRACE RPAREN SEMICOLON STRINGfor_loop : FOR LPAREN INT ID EQUALS NUM SEMICOLON ID LEQ NUM SEMICOLON ID PLUS PLUS RPAREN LBRACE ID DOT ID DOT ID LPAREN ID PLUS NUM RPAREN  SEMICOLON RBRACE'
    
_lr_action_items = {'FOR':([0,],[2,]),'$end':([1,29,],[0,-1,]),'LPAREN':([2,22,],[3,23,]),'INT':([3,],[4,]),'ID':([4,8,12,17,19,21,23,],[5,9,13,18,20,22,24,]),'EQUALS':([5,],[6,]),'NUM':([6,10,25,],[7,11,26,]),'SEMICOLON':([7,11,27,],[8,12,28,]),'LEQ':([9,],[10,]),'PLUS':([13,14,24,],[14,15,25,]),'RPAREN':([15,26,],[16,27,]),'LBRACE':([16,],[17,]),'DOT':([18,20,],[19,21,]),'RBRACE':([28,],[29,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'for_loop':([0,],[1,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> for_loop","S'",1,None,None,None),
  ('for_loop -> FOR LPAREN INT ID EQUALS NUM SEMICOLON ID LEQ NUM SEMICOLON ID PLUS PLUS RPAREN LBRACE ID DOT ID DOT ID LPAREN ID PLUS NUM RPAREN SEMICOLON RBRACE','for_loop',28,'p_for_loop','Analizador Sintactico.py',66),
]