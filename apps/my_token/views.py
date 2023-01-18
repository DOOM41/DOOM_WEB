# Python
from typing import Any, Type
from abstracts.mixins import PayMixin

# Django
from settings.conf import web3, MNEMONIC, ABI

# REST
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# APPS
from transactions.models import Transactions
from bank_account.models import BankAccount

# THIRDAPPS
from solcx import compile_source
from web3 import Account
# Create your views here.


class AddContracts(ModelViewSet, ListAPIView, PayMixin):
    queryset = Transactions.objects.all()

    def list(self, request):
        compiled_sol = compile_source(
            '''//SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

contract Token {
    uint256 public totalSuppl = 1000000e18;
    mapping(address => uint256) public balancOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => bool) public blackList;
    address public owner;
    string public name = "DOOM";
    string public symbol = "DT";
    uint8 public decimal = 18;
    uint16 private PRIZE_FOR_YEARE = 10;
    struct Stake {
        uint256 amount;
        uint256 timestamp;
    }
    mapping(address => Stake) private stakes;

    constructor() {
        owner = msg.sender;
        mint();
    }

    function staking(uint256 amount) external returns (bool) {
        require(!blackList[msg.sender], "You are in blackList");
        require(balancOf[msg.sender] >= amount, "You don't have enough money");
        stakes[msg.sender] = Stake(amount, block.timestamp);
        balancOf[msg.sender] -= amount;
        return true;
    }

    function getAllFromStaking() external returns (uint) {
        require(!blackList[msg.sender], "You are in blackList");
        require(stakes[msg.sender].amount != 0, "You don't have stake money");
        uint days_lying = ((block.timestamp - stakes[msg.sender].timestamp) / (3600 * 24));
        uint bonus = ((stakes[msg.sender].amount*days_lying)/365)/PRIZE_FOR_YEARE;
        balancOf[msg.sender] += stakes[msg.sender].amount + bonus;
        stakes[msg.sender].amount = 0;
        return bonus;
    }

    function addToBlackList(address bad_guy) external returns (bool) {
        require(msg.sender == owner, "You are not token owner");
        require(!blackList[bad_guy], "He is in black list");
        blackList[bad_guy] = true;
        return true;
    }

    function totalSupply() external view returns (uint256) {
        return totalSuppl;
    }

    function balanceOf(address account) external view returns (uint256) {
        return balancOf[account];
    }

    function transfer(address recipient, uint256 amount)
        external
        returns (bool)
    {
        require(msg.sender != recipient, "You can't send money to yourself!");
        require(!blackList[msg.sender], "You are in blackList");
        balancOf[msg.sender] -= amount;
        balancOf[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function allowanc(address owne, address spender)
        external
        view
        returns (uint256)
    {
        return allowance[owne][spender];
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approve(msg.sender, spender, amount);
        return true;
    }

    function mint() public {
        require(!blackList[msg.sender], "You are in blackList");
        balancOf[msg.sender] = 500e18;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool) {
        allowance[sender][recipient] -= amount;
        balancOf[sender] -= amount;
        balancOf[recipient] += amount;
        emit Transfer(sender, recipient, amount);
        return true;
    }

    event Transfer(address indexed from, address indexed to, uint256 amount);
    event Approve(
        address indexed owner,
        address indexed spender,
        uint256 amount
    );
}
''',
            output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_sol.popitem()
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']
        web3.eth.default_account = web3.eth.account.from_mnemonic(
            MNEMONIC).address
        # breakpoint()
        # print(web3.eth.account.from_mnemonic(MNEMONIC))
        con = web3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = con.constructor().transact()
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return Response(
            data={
                'abi': abi,
                'contract_id': str(tx_receipt.contractAddress),
            },
            status=201
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='token-transact',
        # permission_classes=(
        #     IsAuthenticated,
        # )
    )
    def get_my_getted_transactions(self, request: Request):
        # Contract
        con_address = '0x418b12248dfa801Aa664D0D07cF57677e36c4864'
        greeter = web3.eth.contract(
            address=con_address,
            abi=ABI
        )

        # addreses
        some_addres: BankAccount = BankAccount.objects.get(id=2)
        account: Account = Account.from_key(some_addres.private_key)
        web3.eth._default_account = account._address
        to: BankAccount = BankAccount.objects.get(id=1)

        # functions
        trans = greeter.functions.transfer(
            to.address, 10*(10**18)).transact()
        tx_receipt = web3.eth.wait_for_transaction_receipt(trans)
        account.sign_transaction(tx_receipt)
        from_ = greeter.functions.balanceOf(some_addres.address).call()
        second = greeter.functions.balanceOf(to.address).call()
        # result = web3.eth.accounts

        return Response(
            data={
                'from': from_,
                'to': second,
                'tx_receipt': trans,
            },
            status=201
        )
    
    @action(
        methods=['get'],
        detail=False,
        url_path='test',
        # permission_classes=(
        #     IsAuthenticated,
        # )
    )
    def get_my_getted_transas(self, request: Request):
        some_addres: BankAccount = BankAccount.objects.get(id=2)

        acc = web3.eth.account.create()

        return Response(
            data={
                'acc': acc
            },
            status=201
        )
