~dynamic_run_opcode = "";
.dynamic_run_end = 0x60;

void dynamic_run: ~opcodes{;
    ~dynamic_run_opcode = ~opcodes;
    asm_entry: "4C  @var_adress:~dynamic_run_opcode|"; // run the opcode
}
