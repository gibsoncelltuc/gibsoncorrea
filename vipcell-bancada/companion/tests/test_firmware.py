import http.server, os, socket, sys, threading, hashlib, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vipbench import firmware  # noqa: E402

def test_advise_tem_regra_rollback():
    linhas = "\n".join(firmware.advise(firmware.DeviceInfo(product="fogo")))
    assert "anti-rollback" in linhas.lower()
    assert "fogo" in linhas

def _serve(payload):
    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers(); self.wfile.write(payload)
        def log_message(self, *a): pass
    s = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=s.handle_request, daemon=True).start()
    return s.server_address[1]

def test_download_verifica_hash_ok():
    payload = b"firmware-oficial-exemplo" * 1000
    sha = hashlib.sha256(payload).hexdigest()
    port = _serve(payload)
    with tempfile.TemporaryDirectory() as d:
        dest = os.path.join(d, "fw.zip")
        firmware.download(f"http://127.0.0.1:{port}/fw.zip", dest, sha)
        assert os.path.getsize(dest) == len(payload)

def test_download_hash_errado_recusa():
    payload = b"conteudo"
    port = _serve(payload)
    with tempfile.TemporaryDirectory() as d:
        dest = os.path.join(d, "fw.zip")
        try:
            firmware.download(f"http://127.0.0.1:{port}/fw.zip", dest, "00"*32)
            assert False, "deveria recusar hash errado"
        except ValueError as e:
            assert "hash" in str(e).lower()

if __name__ == "__main__":
    fns = [v for k,v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print(f"  ok  {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} testes passaram")
