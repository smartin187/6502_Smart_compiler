import "dynamic_run/dynamic_run.sma";

~read_op_codes = [0xAD, 0x00, 0x00, 0x60]; // the 2 0x00 will be the address
~write_op_codes = [0xA9, 0x00, 0x8D, 0x00, 0x00, 0x60];

.read_get_address = 0;


void read_simple: .read_address_1, .read_address_2{;

    ~read_op_codes[1] = .read_address_2;
    ~read_op_codes[2] = .read_address_1;

    dynamic_run: ~read_op_codes;

    asm_entry: "8D @var_adress:.read_get_address|"; // store the value in the variable

    return .read_get_address;
}

void write_simple: .write_address_1, .write_address_2, .value{;

    ~write_op_codes[1] = .value;

    ~write_op_codes[3] = .write_address_1;
    ~write_op_codes[4] = .write_address_2;

    dynamic_run: ~write_op_codes;
}