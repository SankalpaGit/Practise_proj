import http.server
import socketserver
import urllib.parse

PORT = 8000 #where ptoject run

class BODMASHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/calculate"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            expression = params.get("expression", [""])[0]
            
            try:
                result = self.evaluate_expression(expression)
                response = f"Result: {result}"
            except Exception as e:
                response = f"Error: {str(e)}"
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(response, "utf8"))
        else:
            if self.path == '/':
                self.path = '/page.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def evaluate_expression(self, expression):
        import re
        def parse_expression(expr):
            expr = expr.replace('{', '(').replace('}', ')').replace('[', '(').replace(']', ')')
            return eval_expr(expr)
        
        def eval_expr(expr):
            def helper(tokens):
                stack = []
                num = 0
                sign = 1
                while tokens:
                    token = tokens.pop(0)
                    if token.isdigit():
                        num = num * 10 + int(token)
                    elif token in '+-*/':
                        stack.append(sign * num)
                        num = 0
                        sign = 1 if token == '+' else -1 if token == '-' else token
                    elif token == '(':
                        num = helper(tokens)
                    elif token == ')':
                        break
                    else:
                        raise ValueError("Invalid character in expression")
                stack.append(sign * num)
                return sum(stack)
            if re.search(r'[^0-9+\-*/(){}[\] ]', expr):
                raise ValueError("Invalid characters in expression")
            
            tokens = re.findall(r'\d+|[-+*/()]', expr)
            return helper(tokens)
        
        return parse_expression(expression)

with socketserver.TCPServer(("", PORT), BODMASHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
