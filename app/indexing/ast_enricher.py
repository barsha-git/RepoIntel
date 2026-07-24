"""AST enrichment utilities."""

import ast

from langchain_core.documents import Document

class ASTEnricher:
    """Enrich Python source files with AST metadata."""

    def enrich(self, documents: list[Document],) -> list[Document]:
        """Enrich a list of documents with AST metadata."""

        enriched_documents: list[Document] = []

        for document in documents:
            if document.metadata.get("extension") != ".py":
                enriched_documents.append(document)
                continue

            enriched_documents.append(
                self._enrich_python_document(document)
            )

        return enriched_documents

    def _enrich_python_document(self, document: Document) -> Document:
        """Enrich a Python document with AST metadata."""

        try:
            tree = ast.parse(document.page_content)
        except SyntaxError:
            # Skip files with invalid Python syntax.
            return document

        metadata = {
            "imports": self._extract_imports(tree),
            "classes": self._extract_classes(tree),
            "functions": self._extract_functions(tree),
        }

        document.metadata.update(metadata)

        return document

    def _extract_imports(self, tree: ast.AST,) -> list[str]:
        """Extract imported modules."""

        imports: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(
                    alias.name
                    for alias in node.names
                )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                imports.extend(
                    f"{module}.{alias.name}"
                    for alias in node.names
                )

        return imports

    def _extract_classes(self, tree: ast.AST) -> list[str]:
        """Extract class names."""

        return [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

    def _extract_functions(self, tree: ast.AST) -> list[str]:
        """Extract function names."""

        return [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]
