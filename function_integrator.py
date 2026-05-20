"""
Интегрирует элементарные функции: экспоненты, тригонометрические
"""

import re


class FunctionIntegrator:
    def __init__(self, expr: str, var: str):
        self.expr = expr
        self.var = var

    def integrate(self):
        expr = self.expr.strip()
        var = self.var

        # 1. ∫ dx
        if expr == "1":
            return var

        # 2. ∫ k dx
        if expr.isdigit():
            return f"{expr}{var}"

        # 3. ∫ x^m dx
        match = re.match(rf'{re.escape(var)}\^(\d+)$', expr)
        if match:
            m = int(match.group(1))
            if m != -1:
                return f"{var}^{m+1}/{m+1}"

        # 4. ∫ dx/x^2
        if expr == f"1/{var}^2":
            return f"-1/{var}"

        # 5. ∫ dx/√x
        if expr == f"1/sqrt({var})":
            return f"2*sqrt({var})"

        # 6. ∫ √x dx
        if expr == f"sqrt({var})":
            return f"2/3{var}^(3/2)"

        # 7. ∫ dx/x
        if expr == f"1/{var}":
            return f"ln|{var}|"

        # 8. ∫ dx/(x +- a)
        match = re.match(rf'1/\({re.escape(var)}\+(\d+)\)', expr)
        if match:
            a = match.group(1)
            return f"ln|{var}+{a}|"
        match = re.match(rf'1/\({re.escape(var)}-(\d+)\)', expr)
        if match:
            a = match.group(1)
            return f"ln|{var}-{a}|"

        # 9. ∫ e^x dx
        if expr == f"e^{var}":
            return f"e^{var}"

        # 10. ∫ a^x dx
        match = re.match(r'^(\d+)\^x$', expr)
        if match:
            a = match.group(1)
            return f"{a}^{var}/ln({a})"

        # 11. ∫ cos x dx
        if expr == f"cos({var})":
            return f"sin({var})"

        # 12. ∫ cos kx dx
        match = re.match(rf'cos\((\d+){re.escape(var)}\)', expr)
        if match:
            k = match.group(1)
            return f"1/{k}sin({k}{var})"

        # 13. ∫ sin x dx
        if expr == f"sin({var})":
            return f"-cos({var})"

        # 14. ∫ sin kx dx
        match = re.match(rf'sin\((\d+){re.escape(var)}\)', expr)
        if match:
            k = match.group(1)
            return f"-1/{k}cos({k}{var})"

        # 15. ∫ dx/cos^2 x
        if expr == f"1/cos({var})^2":
            return f"tg({var})"

        # 16. ∫ dx/sin^2 x
        if expr == f"1/sin({var})^2":
            return f"-ctg({var})"

        # 17. ∫ dx/√(1-x^2)
        if expr == f"1/sqrt(1-{var}^2)":
            return f"arcsin({var})"

        # 18. ∫ dx/(1+x^2)
        if expr == f"1/(1+{var}^2)":
            return f"arctg({var})"

        # 19. ∫ tg x dx
        if expr == f"tg({var})":
            return f"-ln|cos({var})|"

        # 20. ∫ ctg x dx
        if expr == f"ctg({var})":
            return f"ln|sin({var})|"

        # 21. ∫ e^(kx) dx
        match = re.match(rf'e\^\((\d+){re.escape(var)}\)', expr)
        if match:
            k = match.group(1)
            return f"1/{k}e^({k}{var})"

        # 22. ∫ dx/√(a^2 - x^2)
        match = re.match(rf'1/sqrt\((\d+)-{re.escape(var)}\^2\)', expr)
        if match:
            a_sq = int(match.group(1))
            a = int(a_sq ** 0.5)
            return f"arcsin({var}/{a})"

        # 23. ∫ dx/(a^2 + x^2)
        match = re.match(rf'1/\((\d+)\+{re.escape(var)}\^2\)', expr)
        if match:
            a_sq = int(match.group(1))
            a = int(a_sq ** 0.5)
            return f"1/{a}arctg({var}/{a})"

        # 24. ∫ dx/(x^2 - a^2)
        match = re.match(rf'1/\({re.escape(var)}\^2-(\d+)\)', expr)
        if match:
            a_sq = int(match.group(1))
            a = int(a_sq ** 0.5)
            return f"1/{2*a}ln|({var}-{a})/({var}+{a})|"

        # 25. ∫ dx/√(x^2 + a^2)
        match = re.match(rf'1/sqrt\({re.escape(var)}\^2\+(\d+)\)', expr)
        if match:
            a_sq = int(match.group(1))
            a = int(a_sq ** 0.5)
            return f"ln|{var} + sqrt({var}^2+{a_sq})|"

        # 26. ∫ dx/√(x^2 - a^2)
        match = re.match(rf'1/sqrt\({re.escape(var)}\^2-(\d+)\)', expr)
        if match:
            a_sq = int(match.group(1))
            a = int(a_sq ** 0.5)
            return f"ln|{var} + sqrt({var}^2-{a_sq})|"

        return None