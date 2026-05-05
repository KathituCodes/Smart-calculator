import streamlit as st
import ast
import operator

# Define supported operators
OPERATORS = {
    ast.Add: operator.add, 
    ast.Sub: operator.sub, 
    ast.Mult: operator.mul,
    ast.Div: operator.truediv, 
    ast.Pow: operator.pow, 
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

def safe_eval(node):
    # Handle Numbers (Modern Python 3.8+)
    if isinstance(node, ast.Constant): 
        if isinstance(node.value, (int, float)):
            return node.value
    
    # Legacy support (for older environments, though usually not needed now)
    elif hasattr(ast, 'Num') and isinstance(node, ast.Num):
        return node.n
        
    # Handle Binary Operations (e.g., 1 + 1)
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        return OPERATORS[type(node.op)](left, right)
    
    # Handle Unary Operations (e.g., -5)
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        return OPERATORS[type(node.op)](operand)
    
    else:
        raise TypeError(f"Unsupported expression type: {type(node)}")

# --- Streamlit Interface ---
st.title("Smart Calculator")
st.write("Enter a mathematical expression (e.g., `(5 + 3) * 2`)")

expr = st.text_input("Expression:", "10 + 5 / 2")

if st.button("Calculate"):
    try:
        # Parse the expression into an AST
        # mode='eval' ensures only a single expression is allowed
        node = ast.parse(expr, mode='eval').body
        result = safe_eval(node)
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Invalid Expression: {e}")
