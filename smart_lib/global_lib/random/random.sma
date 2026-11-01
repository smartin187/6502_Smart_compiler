import "assembly/advenced_operation.sma";
import "assembly/simple_operation.sma";

.random_keep_value = 0; // variable were save the value of register for sum.

.random_value_a = 0; // the value will be the random value.

def random_sum{;
    // This function sum the value of A, X, Y, stack ptr

    // On all ADC, the carry flag is never remove before the ADC, because it add ramdom...

    // Save X at .random_keep_value and add to A
    asm_entry: "STX_ABS @var_adress:.random_keep_value| ";
    asm_entry: "ADC_ABS @var_adress:.random_keep_value| ";

    // Save Y at .random_keep_value and add to A
    asm_entry: "STY_ABS @var_adress:.random_keep_value| ";
    asm_entry: "ADC_ABS @var_adress:.random_keep_value| ";

    // Trasfet stack ptr to X and save X at .random_keep_value and add to A
    TSX;
    asm_entry: "STX_ABS @var_adress:.random_keep_value| ";
    asm_entry: "ADC_ABS @var_adress:.random_keep_value| ";

    asm_entry: "STA_ABS @var_adress:.random_value_a| "; // Save the value of A at .random_value_a

    return .random_value_a;
}

//def random_256{;
//}