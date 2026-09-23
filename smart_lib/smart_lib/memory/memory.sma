import "dynamic_run/dynamic_run.sma";

~read_op_codes = [0xAD, 0x00, 0x00, 0x60]; // the 2 0x00 will be the address

.read_get_address = 0;


void read_simple: .read_address_1, .read_address_2{;

    ~read_op_codes[1] = .read_address_2;
    ~read_op_codes[2] = .read_address_1;

    dynamic_run: ~read_op_codes;

    asm_entry: "8D @var_adress:.read_get_address|"; // store the value in the variable

    return .read_get_address;

}