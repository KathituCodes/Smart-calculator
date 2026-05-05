import streamlit as st
import operator as op

class SmartCalculator:
    def __init__(self):
        self.operators = {
            ast.Add: op.add, ast.Sub: op.sub, 
            ast.Mult: op.mul, ast.Div: op.truediv, 
            ast.Pow: op.pow, ast.USub: op.neg
        }

    def evaluate(self, expression: str):
        try:
            node = ast.parse(expression, mode='eval').body
            return self._eval_node(node)
        except Exception as e:
            return f"Error: {e}"

    def _eval_node(self, node):
        if isinstance(node, (ast.Num, ast.Constant)):
            return node.n if hasattr(node, 'n') else node.value
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](
                self._eval_node(node.left), 
                self._eval_node(node.right)
            )
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](
                self._eval_node(node.operand)
            )
        else:
            raise TypeError("Invalid Syntax")

def main():
    st.set_page_config(page_title="Advanced Smart Calc", layout="wide")
    
    # --- UI Header ---
    st.title("🚀 Advanced Interactive Calculator")
    st.write("A secure, AST-based mathematical engine with multi-mode input.")

    calc = SmartCalculator()

    # --- Sidebar Configuration ---
    st.sidebar.header("Settings")
    precision = st.sidebar.slider("Decimal Precision", 0, 10, 2)
    theme_color = st.sidebar.color_picker("Result Highlight Color", "#00FFAA")

    # --- Main Interface ---
    tab1, tab2 = st.tabs(["Custom Expression", "Step-by-Step Builder"])

    with tab1:
        st.subheader("Free-form Syntax")
        raw_expr = st.text_input("Enter complex formula:", placeholder="(2 + 3) ** 2 / 5")
        if st.button("Evaluate Formula"):
            process_result(calc, raw_expr, precision, theme_color)

    with tab2:
        st.subheader("Operation Builder")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            val1 = st.number_input("First Value", value=0.0)
        with col2:
            operation = st.selectbox("Operation", ["+", "-", "*", "/", "**"])
        with col3:
            val2 = st.number_input("Second Value", value=0.0)

        if st.button("Run Builder"):
            builder_expr = f"{val1} {operation} {val2}"
            process_result(calc, builder_expr, precision, theme_color)

def process_result(engine, expression, precision, color):
    if expression:
        res = engine.evaluate(expression)
        if isinstance(res, (int, float)):
            formatted_res = round(res, precision)
            st.markdown(f"### Result")
            st.code(formatted_res, language="python")
            st.balloons()
        else:
            st.error(res)

if __name__ == "__main__":
    main()
