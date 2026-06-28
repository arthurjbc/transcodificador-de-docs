import markdown


def convert(source_format: str, target_format: str, data: bytes) -> bytes:
    if (source_format, target_format) == ("markdown", "html"):
        return markdown.markdown(data.decode("utf-8")).encode("utf-8")

    raise NotImplementedError(
        f"conversão de '{source_format}' para '{target_format}' não suportada"
    )
