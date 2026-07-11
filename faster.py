import json
import base64
import asyncio
import httpx
import sys
import logging
from Crypto.Cipher import AES
from flask import Flask, request, jsonify
from google.protobuf import json_format
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor_pool as _descriptor_pool
from functools import lru_cache
import time

# =====================================================================
# LOGGING SETUP
# =====================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====================================================================
# PROTOBUF DEFINITIONS - COMPLETE
# =====================================================================

# --- FreeFire.proto ---
ff_proto = b'\n\x0e\x46reeFire.proto\"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d \x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t\"]\n\x10\x42lacklistInfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\r\"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\"\xa0\x03\n\x08LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME_AUTO_NEW\x10\xf6\x07\x62\x06proto3'

DESCRIPTOR_FF = _descriptor_pool.Default().AddSerializedFile(ff_proto)
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_FF, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_FF, 'FreeFire_pb2', globals())

# --- Get LoginReq and LoginRes classes ---
LoginReq = globals()['LoginReq']
LoginRes = globals()['LoginRes']

# =====================================================================
# FLASK APP SETUP
# =====================================================================
app = Flask(__name__)

# === Constants ===
MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"
RELEASEVERSION = "OB54"

# === HTTP Client Pool ===
_client = None

def get_client():
    global _client
    if _client is None:
        limits = httpx.Limits(max_keepalive_connections=100, max_connections=200)
        _client = httpx.Client(
            timeout=httpx.Timeout(30.0, connect=5.0),
            limits=limits,
            http2=True,
            follow_redirects=True
        )
    return _client

# === AES Encryption ===
def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    padding_length = AES.block_size - (len(plaintext) % AES.block_size)
    padded = plaintext + bytes([padding_length] * padding_length)
    return aes.encrypt(padded)

# === JWT Generation ===
def create_jwt(uid: str, password: str):
    try:
        # Step 1: Get Access Token
        url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
        payload = f"uid={uid}&password={password}&response_type=token&client_type=2&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
        headers = {
            'User-Agent': USERAGENT,
            'Content-Type': "application/x-www-form-urlencoded"
        }
        client = get_client()
        resp = client.post(url, data=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        access_token = data.get("access_token", "0")
        open_id = data.get("open_id", "0")
        
        if access_token == "0" or open_id == "0":
            raise Exception("Failed to get access token")
        
        # Step 2: Create LoginReq protobuf
        login_req = LoginReq()
        login_req.open_id = open_id
        login_req.open_id_type = "4"
        login_req.login_token = access_token
        login_req.orign_platform_type = "4"
        
        proto_bytes = login_req.SerializeToString()
        encrypted = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)
        
        # Step 3: Send to MajorLogin
        url = "https://loginbp.ggblueshark.com/MajorLogin"
        headers = {
            'User-Agent': USERAGENT,
            'Content-Type': "application/octet-stream",
            'X-Unity-Version': "2022.3.47f1",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASEVERSION
        }
        resp = client.post(url, data=encrypted, headers=headers)
        resp.raise_for_status()
        
        # Step 4: Parse LoginRes
        login_res = LoginRes()
        login_res.ParseFromString(resp.content)
        
        return {
            'token': login_res.token if login_res.token else '0',
            'region': login_res.lock_region if login_res.lock_region else '0',
            'server_url': login_res.server_url if login_res.server_url else '0'
        }
    except Exception as e:
        logger.error(f"JWT creation failed: {e}")
        raise

# === API Routes ===
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "🔥 Super Fast JWT Generator", "version": RELEASEVERSION}), 200

@app.route('/api/token', methods=['GET'])
def get_jwt():
    start = time.time()
    uid = request.args.get('uid')
    password = request.args.get('password')
    
    if not uid or not password:
        return jsonify({"error": "uid and password required"}), 400
    
    try:
        result = create_jwt(uid, password)
        elapsed = round((time.time() - start) * 1000, 2)
        result['response_time_ms'] = elapsed
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/decode', methods=['GET'])
def decode_jwt():
    jwt_token = request.args.get('jwt') or request.args.get('token')
    if not jwt_token:
        return jsonify({"error": "Provide jwt or token param"}), 400
    
    parts = jwt_token.split('.')
    if len(parts) < 2:
        return jsonify({"error": "Malformed JWT"}), 400
    
    def b64url_decode(s):
        s = s.replace('-', '+').replace('_', '/')
        padding = len(s) % 4
        if padding:
            s += '=' * (4 - padding)
        return base64.b64decode(s)
    
    try:
        header = json.loads(b64url_decode(parts[0]).decode())
        payload = json.loads(b64url_decode(parts[1]).decode())
        sig = parts[2] if len(parts) > 2 else ""
        return jsonify({"header": header, "payload": payload, "signature": sig}), 200
    except Exception as e:
        return jsonify({"error": f"Decode failed: {str(e)}"}), 400

# === Run ===
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"[🔥] Super Fast DEVILS WILL RISE JWT Generator on port {port}")
    print(f"[⚡] Owner: @arafatpramaniksiam | Channel: @arafatcodex")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)