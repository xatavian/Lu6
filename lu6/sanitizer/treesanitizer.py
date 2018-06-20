from ..syntaxtree import CompilationUnit, ClassDeclaration, FunctionDeclaration, \
                         ClassCategory, ClassBody,  MethodDeclaration, AttributeDeclaration
from ..syntaxtree.modifier import PRIVATE, PROTECTED, PUBLIC
from ..exceptions import TemplateEngineException
from .contextsanitizer import ContextSanitizer


class TreeSanitizer(object):
    @staticmethod
    def build_codegen_tree(ast):
        if not isinstance(ast, CompilationUnit):
            raise TemplateEngineException("Error during tree sanitizing", -1)

        result = CompilationUnit(ast.filename, ast.line, ast.includes, [])

        for type_decl in ast.type_declarations:
            result.type_declarations.append(
                TreeSanitizer.sanitize_type_declaration(type_decl)
            )

        result.context = ContextSanitizer.sanitize_context(ast.context)
        return result

    @staticmethod
    def sanitize_type_declaration(type_decl):
        if not isinstance(type_decl, ClassDeclaration) and not isinstance(type_decl, FunctionDeclaration):
            raise TemplateEngineException("Error during tree sanitizing", -1)

        if isinstance(type_decl, ClassDeclaration):

            result = ClassDeclaration(
                type_decl.line,
                type_decl.class_name,
                type_decl.extends_name,
                TreeSanitizer.sanitize_class_body(type_decl.class_body)
            )
            result.context = ContextSanitizer.sanitize_context(type_decl.context)
            return result
        else:
            raise TemplateEngineException("Tree sanitizing of functions are not supported yet", -1)

    @staticmethod
    def sanitize_class_body(class_body):
        # Categories for methods
        method_categories = {
            "public": ClassCategory(class_body.line, "public"),
            "private" : ClassCategory(class_body.line, "private"),
            "protected": ClassCategory(class_body.line, "protected")
        }

        # Categories for attributes
        attribute_categories = {
            "public": ClassCategory(class_body.line, "public"),
            "private": ClassCategory(class_body.line, "private"),
            "protected": ClassCategory(class_body.line, "protected")
        }

        others = []

        for member in class_body.members:
            sanitized = TreeSanitizer.sanitize_member_declaration(member)
            TreeSanitizer._inject_in_categories(sanitized, method_categories, attribute_categories, others)

        result = ClassBody(class_body.line, [
            method_categories["public"], method_categories["private"], method_categories["protected"],
            attribute_categories["public"], attribute_categories["protected"], attribute_categories["private"]
        ])
        result.context = ContextSanitizer.sanitize_context(class_body.context)
        return result

    @staticmethod
    def sanitize_member_declaration(member):
        if isinstance(member, MethodDeclaration):
            member.context = ContextSanitizer.sanitize_context(member.context)
            return member
        elif isinstance(member, AttributeDeclaration):
            member.context = ContextSanitizer.sanitize_context(member.context)
            return member

    @staticmethod
    def _inject_in_categories(elmt, method_categories, attribute_categories, others):
        if isinstance(elmt, MethodDeclaration):
            if PUBLIC in elmt.modifiers:
                method_categories["public"].declarations.append(elmt)
            elif PROTECTED in elmt.modifiers:
                method_categories["protected"].declarations.append(elmt)
            elif PRIVATE in elmt.modifiers:
                method_categories["private"].declarations.append(elmt)
            else:
                print("Error during category injection")

        elif isinstance(elmt, AttributeDeclaration):
            if PUBLIC in elmt.modifiers:
                attribute_categories["public"].declarations.append(elmt)
            elif PROTECTED in elmt.modifiers:
                attribute_categories["protected"].declarations.append(elmt)
            elif PRIVATE in elmt.modifiers:
                attribute_categories["private"].declarations.append(elmt)
            else:
                print("Error during category injection")

        elif isinstance(elmt, ClassCategory):
            others.append(elmt)

        elif isinstance(elmt, list):
            for ee in elmt:
                TreeSanitizer._inject_in_categories(ee, method_categories, attribute_categories, others)

        else:
            raise TemplateEngineException("Error during member injection", -1)