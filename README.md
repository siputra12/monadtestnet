# **Monad Testnet Automation Script**
This is a Python script to easily interact with various ecosystems on the Monad Testnet — including swap, liquidity, deposit, and faucet operations — across multiple projects.

---

## 🌟 Supported Ecosystems
- **Octoswap** — Swap, Add Liquidity, Remove Liquidity

- **Bean Exchange** — Swap, Add Liquidity, Remove Liquidity

- **Taya Swap** — Swap, Add Liquidity, Remove Liquidity

- **Monorail** — Swap

- **Shmond** — Deposit, Withdraw, Commit, Uncommit

- **Monad Swap** — Swap (CHOG, YAKI, DAK)

- **Nitro Finance** — Claim Faucet, Swap

- **Mudigital** — Deposit MuBond

- **Curvance** — Claim Faucet, Deposit USDC, Swap, Lock CVE

- **Magma Stakes** — Deposit, Withdraw

**You can also [click here](http://www.zerox.pro/data/tasks.json) to see all tasks.**

---

### ⚙️ Requirements
- **Python 3.10**
- **Node.js (latest version)**

---

### 🛠️ Installation
- **Install the required Python packages:**
```bash
pip install web3==5.30.0 prompt_toolkit
```

---

### 🚀 How to Use
- **Prepare your wallets in ```wallet.monad``` file using the following format (each wallet on a new line):**

```ADDRESS\tPRIVATE_KEY```

- **Run the setup script:**

```bash
python3.10 monad.py setup
```
Select and check all ecosystems you want to operate on, then click **Done**.

- **To run the script across all wallets, use:**

```bash
python3.10 monad.py intervalFrom,intervalTo
```
Example: 
```bash
python3.10 monad.py 10,15
```

Select the wallets you want to use.

OR

To run the script for a specific wallet line:

```bash
python3.10 monad.py intervalFrom,intervalTo wallet_line
```
Example: 
```bash
python3.10 monad.py 10,15 1
```

This will run only for the wallet on line 1.

### 📌 Notes
Make sure your wallets are funded with testnet tokens.

Always double-check your private keys handling to avoid errors.

This script is optimized for Python 3.10.
