from prompt_toolkit.shortcuts import radiolist_dialog, checkboxlist_dialog
import json, random, importlib, time, os, sys, requests
from web3 import Web3, Account
from eth_account.messages import SignableMessage

abi_contract = [
    {
        "type": "function",
        "name": "approve",
        "inputs": [{
            "name": "spender",
            "type": "address",
            "internalType": "address"
        }, {
            "name": "amount",
            "type": "uint256",
            "internalType": "uint256"
        }],
        "outputs": [],
        "stateMutability": "payable"
    }, {
        "type": "function",
        "name": "allowance",
        "inputs": [{
            "name": "owner",
            "type": "address",
            "internalType": "address"
        }, {
            "name": "spender",
            "type": "address",
            "internalType": "address"
        }],
        "outputs": [{
            "name": "",
            "type": "uint256",
            "internalType": "uint256"
        }],
        "stateMutability": "view"
    }, {
        "type": "function",
        "name": "balanceOf",
        "inputs": [{
            "name": "account",
            "type": "address",
            "internalType": "address"
        }],
        "outputs": [{
            "name": "",
            "type": "uint256",
            "internalType": "uint256"
        }],
        "stateMutability": "view"
    }
]
d_path = os.path.join(os.getcwd(), 'data')
l_path = os.path.join(os.getcwd(), 'logs')
def shuffle_datas(od):
    new_keys = []
    for key in od:
        new_keys.append(key)
    random.shuffle(new_keys)
    datas = {}
    for key in new_keys:
        datas[key] = od[key]
    return datas

def get_logs(fname):
    with open(os.path.join(l_path, f"{fname}.json"), 'r') as f:
        return json.load(f)

def get_data(fnames):
    fname = os.path.join(d_path, f"{fname}.json")
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            return json.load(f)
    else:
        return requests.get(f"http://www.zerox.pro/data/{fnames}.json").json()

def input_logs(fname, jdata):
    with open(os.path.join(l_path, f"{fname}.json"), 'w') as f:
        json.dump(jdata, f, indent=4)

def input_data(fname, jdata):
    with open(os.path.join(d_path, f"{fname}.json"), 'w') as f:
        json.dump(jdata, f, indent=4)
if len(sys.argv) < 2:
    os._exit(1)

if sys.argv[1] == "setup":
    options = [
        ("monadswap", "Monad Swap"),
        ("monorail", "Monorail"),
        ("taya", "Taya"),
        ("curvance", "Curvance"),
        ("magmastake", "Magma Stake"),
        ("mudigital", "MuDigital"),
        ("nitro", "Nitro Finance"),
        ("octoswap", "Octo Swap"),
        ("shmond", "ShMond"),
        ("bean", "Bean Exchange")
    ]
    result = checkboxlist_dialog(
        title="⚙️ Task Configuration",
        text="Choose Task You Want:",
        values=options,
        ok_text="Done",
        cancel_text="Cancel"
    ).run()
    if result is None:
        print("Setup Canceled!")
    else:
        print("Task Choosen:")
        for r in result:
            print(f"✅ {r}")
        input_data("allowlist_task", result)
    os._exit(1)

if not os.path.isfile(os.path.join(d_path, "allowlist_task.json")):
    executeable = sys.executable.split("/")[-1]
    print(f"⚠️ Before you run, please do : \n{executeable} {sys.argv[0]} setup")
    os._exit(1)

wallets = []
with open("wallet.monad", "r") as f:
    datas = f.readlines()
for data in datas:
    w = data.strip().split("\t")
    if len(w) >= 2:
        wallets.append((w[0], f"{w[1]}:{w[0]}"))

if len(sys.argv) == 2:
    per_page = 5
    page = 0
    while True:
        start = page * per_page
        end = start + per_page
        current_page_wallets = wallets[start:end]
        total_pages = (len(wallets) - 1) // per_page + 1
        extra_controls = [
            ("__prev__", "← Previous") if page > 0 else None,
            ("__next__", "Next →") if end < len(wallets) else None,
        ]
        extra_controls = [item for item in extra_controls if item]
        all_options = [
            (val, f"{start + idx + 1}. {label}") for idx, (label, val) in enumerate(current_page_wallets)
        ] + extra_controls
        result = radiolist_dialog(
            title=f"Wallet List (Page {page+1}/{total_pages})",
            text="Pilih Wallet :",
            values=all_options
        ).run()
        if result == "__next__":
            page += 1
        elif result == "__prev__":
            page -= 1
        elif result == "__exit__" or result is None:
            print("Stopping Program!")
            break
        else:
            break
    if result == "__exit__" or result is None:
        os._exit(1)
else:
    result = wallets[int(sys.argv[2])-1][1]
    del sys.argv[2]
w = result.split(":")
pk = w[0]
sys.argv.append(pk)
address = w[1]
bsc = "https://cosmological-tame-resonance.monad-testnet.quiknode.pro/84ed94f365bde58e2b51be6d0f1c8fa3a8e0a932/"
cid = 10143
web3 = Web3(Web3.HTTPProvider(bsc))
web3.eth.account.enable_unaudited_hdwallet_features()
acct = web3.eth.account.from_key(pk)
datas = shuffle_datas(get_data('tasks'))
di = datas.copy()
bl_task = []

def get_balance(pk):
    acct = web3.eth.account.from_key(pk)
    balance_wei=web3.eth.getBalance(acct.address)
    return str(web3.fromWei(balance_wei, 'ether'))

for ddddd in di.keys():
    if ddddd == "other_task":
        ddddd = "curvance"
    if ddddd not in get_data("allowlist_task"):
        if ddddd in datas:
            del datas[ddddd]
            bl_task.append(ddddd)
def get_args(module, task):
    module_ori = module
    module = f"{address}_{module}"
    match module_ori:
        case "stakeapr":
            return "done", task # hapus saat task claim sudah dikerjakan
            args = [0.1]
            return args, task
        case "curvance":
            gl = get_logs(module)
            args = [1]
            stask = task.split("=")
            if len(stask) > 1:
                args = [int(stask[1])]
                task = stask[0]
            if time.time() - int(gl[args[0]]) < 86400 and task == "claim_token":
                return "done", task
            else:
                gl[args[0]] = int(time.time())
                input_logs(module, gl)
                return args, task
        case "bean":
            gl = get_logs(module)
            if "swap" in task:
                val = gl[0]
            else:
                val = gl[3]
            args = [val, gl[2]]
            return args, task
        case "magmastake":
            gl = get_logs(module)
            args = [gl[0]]
            return args, task
        case "monadswap":
            gl = get_logs(module)
            args = [gl[0], gl[2]]
            return args, task
        case "monorail":
            tasks = task.split("=")
            task = tasks[0]
            gl = get_logs(module)
            if task == "swap_to":
                bal = gl[0]
                t = int(tasks[1])
                f = gl[int(tasks[1])]
                t = "0x0000000000000000000000000000000000000000" if t >= 6 else gl[t+2]
            else:
                bal = gl[0]
                f = "0x0000000000000000000000000000000000000000"
                t = gl[2]
            args = [bal, f, t]
            return args, task.split("_")[0]
        case "mudigital":
            return [random_balance(0.001, 18, 3)], task
        case "nitro":
            gl = get_logs(module)
            tasks = task.split("=")
            task = tasks[0]
            if task == "request_nit":
                glc = int(get_logs(f"{address}_last_claim_nitro")['last_claim'])
                if time.time() - glc < 86400:
                    return "done", task
                else:
                    input_logs(f"{address}_last_claim_nitro", {"last_claim": int(time.time())})
                    args = [0]
            else:
                interv = int(tasks[1])
                if task == "swap_to":
                    f = gl[2]
                    t = gl[interv]
                else:
                    f = gl[interv]
                    t = gl[2]
                bal = gl[0] if task == "swap_to" else "max"
                args = [bal, f, t]
                task = task.split("_")[0]
            return args, task
        case "octoswap":
            gl = get_logs(module)
            bal = gl[3] if 'liquidity' in task else gl[0]
            args = [bal, gl[2]]
            return args, task
        case "shmond":
            gl = get_logs(module)
            return [gl[0]], task
        case "taya":
            gl = get_logs(module)
            bal = gl[3] if "liquidity" in task else gl[0]
            args = [bal, gl[2]]
            return args, task

def random_verified_ticker(bl = []):
    a = 0; vtd = []; pt = ""
    vts = get_data("verified_ticker")
    if len(vts) - len(bl) <= 3:
        for vt in vts:
            if vt['ticker'] not in bl:
                vtd.append(vt)
        random.shuffle(vtd)
        return vtd
    limit = 3 if len(bl) <= 2 else len(vts)-len(bl)
    while True:
        vt = random.choice(vts) if len(vts) > 1 else vts[0]
        if vt['ticker'] == pt or vt['ticker'] in bl:
            continue
        vts.remove(vt)
        if a == limit:
            break
        pt = vt['ticker']
        vtd.append(vt)
        a += 1
    return vtd

def random_nitro(deep = 3):
    pt = ""; vtd = []
    for i in range(0, deep):
        vt = random.choice(get_data("nitro"))
        if vt['symbol'] == pt:
            continue
        else:
            vtd.append(vt)
    return vtd

def random_balance(val = 0, digits = 18, deep_zero = 2):
    return val+(random.randint(int("5" + ("0" * (digits-2))), 10**(digits-1))/10**((digits-2)+deep_zero))

def make_all_logs():
    if not os.path.isfile(f"{l_path}/{address}_last_claim_nitro.json"):
        input_logs(f"{address}_last_claim_nitro", {"last_claim": 0})
    if not os.path.isfile(f"{l_path}/{address}_curvance.json"):
        input_logs(f"{address}_curvance", [0, 0, 0, 0, 0])
    ####################################################BEAN
    vt_bean = random_verified_ticker(["wMON"])[0]
    val_bean = random_balance(0.05)
    val_bean_liq = val_bean/2
    input_logs(f'{address}_bean', [val_bean, vt_bean['ticker'], vt_bean['contract'], val_bean_liq])
    ####################################################MAGMASTAKE
    input_logs(f'{address}_magmastake', [random_balance()])
    ####################################################MONORAIL
    vt_monorail = random_verified_ticker()
    val_monorail = random_balance(0.05)
    input_logs(f'{address}_monorail', [val_monorail, vt_monorail[0]['ticker'], vt_monorail[0]['contract'], vt_monorail[1]['ticker'], vt_monorail[1]['contract'], vt_monorail[2]['ticker'], vt_monorail[2]['contract']])
    ####################################################NITRO
    vt_nitro = random_nitro()
    val_nitro = random_balance(random.randint(5, 15))
    input_logs(f'{address}_nitro', [val_nitro, "NIT", "0xd10047Dc109167Aa52617b74CD8F4E94C90e0479", vt_nitro[0]['symbol'], vt_nitro[0]['address'], vt_nitro[1]['symbol'], vt_nitro[1]['address'], vt_nitro[2]['symbol'], vt_nitro[2]['address']])
    ####################################################OCTOSWAP
    vt_octo = random_verified_ticker(["wMON"])[0]
    val_octo = random_balance(0.1)
    val_octo_liq = val_octo/2
    input_logs(f'{address}_octoswap', [val_octo, vt_octo['ticker'], vt_octo['contract'], val_octo_liq])
    ####################################################SHMOND
    input_logs(f'{address}_shmond', [random_balance(0.05)])
    ####################################################TAYA
    vt_taya = random_verified_ticker(["wMON", "BEAN"])[0]
    val_taya = random_balance(0.1)
    val_taya_liq = val_taya/2
    input_logs(f'{address}_taya', [val_taya, vt_taya['ticker'], vt_taya['contract'], val_taya_liq])
    ####################################################
    ####################################################MONADSWAP
    vt_monadswap = random_verified_ticker(["wMON", "BEAN", "USDC"])[0]
    val_monadswap = random_balance(0.1)
    input_logs(f'{address}_monadswap', [val_monadswap, vt_monadswap['ticker'], vt_monadswap['contract']])
    ####################################################

def delete_all_logs():
    log_name = ["bean", "magmastake", "monorail", "nitro", "octoswap", "shmond", "taya", "monadswap"]
    for n in log_name:
        os.remove(f"{l_path}/{address}_{n}.json")


def sleep_custom(t):
    ce = ["🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚","🕛"]
    i = t; d = 0
    for a in range(0, t):
        print(f"{ce[d]} {time_estimation(i)}..", end="\r")
        i -= 1
        time.sleep(1)
        d += 1
        if d >= 11:
            d = 0

def time_estimation(t):
    te = ""
    d = int(t/86400)
    te += f"{d}d:"
    t = t-(d*86400) if d > 0 else t
    h = int(t/3600)
    te += f"{h}h:"
    t = t-(h*3600) if h > 0 else t
    m = int(t/60)
    te += f"{m}m:"
    t = t-(m*60) if m > 0 else t
    te += f"{t}s"
    return te

def approve(val, contract, CA):
    token = web3.eth.contract(address=Web3.toChecksumAddress(contract), abi=abi_contract)
    bal = token.functions.balanceOf(acct.address).call()
    allow = token.functions.allowance(acct.address, CA).call()
    if allow < bal:
        nonce = web3.eth.getTransactionCount(acct.address, block_identifier='pending')
        airdrop = token.functions.approve(CA, bal)
        gas = int(airdrop.estimateGas({'from': CA})*1.3)
        try:
            data = airdrop.buildTransaction({'chainId':cid,'type': 2,'nonce': nonce, 'value': 0, 'gas': gas})
            signed_tx=web3.eth.account.signTransaction(data, pk)
            tx_hash=web3.toHex(web3.eth.sendRawTransaction(signed_tx.rawTransaction))
            time.sleep(10)
            print("✅ Approve Hash  : " + tx_hash)
        except Exception as E:
            print("⚠️  Error Message :", end="")
            print(E)
    else:
        print("⚠️  Error Message : Already Approved")

CA = {}
def doTask(module, task):
    global CA
    args, task = get_args(module, task)
    if not args:
        return False
    if args == "done":
        return True
    new_args = [task, acct.address]
    for a in args:
        new_args.append(a)
    req = lambda data: requests.post('http://www.zerox.pro:5555/api_web3', json=data).json()['data']
    if 'remove_liquidity' in task:
        if module in ['taya', 'bean']:
            deadline = int(time.time()+600)
            gtdd = req({'module': module, 'data': ['get_typed_data', acct.address, args[-1], deadline]})
            gtd = SignableMessage(
                version=web3.toBytes(hexstr=gtdd['version']),
                body=web3.toBytes(hexstr=gtdd['body']),
                header=web3.toBytes(hexstr=gtdd['header'])
            )
            sm = web3.eth.account.sign_message(gtd, pk)
            sm = {
                "messageHash": sm.messageHash.hex(),
                "r": sm.r,
                "s": sm.s,
                "v": sm.v,
                "signature": sm.signature.hex()
            }
            new_args = new_args + [sm, deadline]
        pair_address = req({'module': module, 'data': ['get_pair', args[-1]]})
    else:
        pair_address = args[-1]
    task_skip_approve = ['claim_token', 'request_nit', 'swap_from', 'deposit','bond','unbond','claim','redeem', 'mint_bond', 'withdraw']
    module_skip_approve = ['monorail']
    if task == "swap" and module == "monorail" and args[-2] != "0x0000000000000000000000000000000000000000":
        approve(web3.toWei(args[0], 'ether'), args[-2], '0xC995498c22a012353FAE7eCC701810D673E25794')
    elif task not in task_skip_approve and module not in module_skip_approve:
        pair_address = "0xB5481b57fF4e23eA7D2fda70f3137b16D0D99118" if task == "lock_cve" else pair_address
        if module == 'nitro':
            CA['nitro'] = "0xFF5DDCF0774006C9B263858F1ad11962bAaaE41C"
            pair_address = args[-2]
        if module == "curvance":
            new_args[2] = random.randint(100, 500) if task == "deposit_usdc" else 1000000
            CA['curvance'] = "0x9E7EbD0f8255F3A910Bc77FD006A410E9D54EE36" if task == "deposit_usdc" else "0x2555223A15a931a71951707cb32A541f14e2c730"
            pair_address = "0x5D876D73f4441D5f2438B1A3e2A51771B337F27A" if task == "deposit_usdc" else "0xB5481b57fF4e23eA7D2fda70f3137b16D0D99118"
        bal = new_args[2] if isinstance(new_args[2], int) else 10000000
        approve(web3.toWei(bal, 'ether'), pair_address, CA[module])
    tx = req({"module": module,"data":new_args})
    if tx:
        tx = json.loads(tx)
        CA[module] = tx['to']
        finish_url = False
        if 'finish_url' in tx:
            finish_url = tx['finish_url']
            del tx['finish_url']
        tx['nonce'] = web3.eth.getTransactionCount(acct.address, block_identifier='pending')
        try:
            signed_tx=web3.eth.account.signTransaction(tx, pk)
            tx_hash=web3.toHex(web3.eth.sendRawTransaction(signed_tx.rawTransaction))
            if finish_url:
                req({"module": module,"data":['finish', address, finish_url, tx_hash]})
            return tx_hash
        except Exception as E:
            return E
    else:
        return True

try:
    args1 = sys.argv[1].split(","); w = []
    for i in args1:
        w.append(i)
    a, b = int(w[0]), int(w[1])
except:
    a, b = 30, 60
make_all_logs()
task_count = sum(len(value) for value in datas.values())
tW = []; sec_est = 0
for _ in range(0, task_count):
    rr = random.randint(a, b)
    sec_est += rr
    tW.append(rr)
est_t = sec_est
old_b = get_balance(pk)
print("==================================")
print("-------Wallet - Information-------")
print("==================================")
print("🔒 Wallet Address : " + address)
print("💰 Wallet Balance : " + old_b)
print("✅ Allowlist Task : ", end="")
print(get_data("allowlist_task"))
print("❌ Blacklist Task : ", end="")
print(bl_task)
print("==================================")
print("🕛 Time Spend Estimation : " + time_estimation(est_t))
tnb = ""; i = 0
while i < task_count:
    datas = shuffle_datas(datas)
    lk = list(datas.keys())
    if len(lk) > 1:
        tn = random.choice(lk)
    elif len(lk) == 1:
        tn = lk[0]
    else:
        break
    if tn == tnb and len(lk) > 1:
        continue
    task = datas[tn][0]
    datas[tn].remove(task)
    if len(datas[tn]) <= 0:
        del datas[tn]
    if tn == "other_task":
        stask = task.split("-")
        tn = stask[0]
        task = stask[1]
    print("==================================")
    print("💼 Project Name  : " + tn.title())
    print("💼 Task Name     : " + task.title())
    print("---------------------------------")
    time.sleep(0.5)
    dt = doTask(tn, task)
    if dt == True or not dt:
        print("⚠️ Error Message : Tx Already Happen or This is Daily Task")
        print("==================================\n\n")
        sleep_custom(5)
        pass
    else:
        print("✅ Tx Hash       : ", end="")
        time.sleep(0.5)
        print(dt)
        print("==================================\n\n")
        sleep_custom(tW[i])
    i += 1
    tnb = tn
new_b = get_balance(pk)
fu = float(old_b) - float(new_b)
print("==================================")
print("💸 MON Used For All Tx : " + str(fu))
print("💰 Current Balance     : " + new_b)
print("==================================")
delete_all_logs()
