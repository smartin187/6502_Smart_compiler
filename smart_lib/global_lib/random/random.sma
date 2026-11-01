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

def random_sub{;
    // This function subtracts X, Y, and the stack pointer from A.

    // Save X at .random_keep_value and subtract it from A
    asm_entry: "STX_ABS @var_adress:.random_keep_value| ";
    asm_entry: "SBC_ABS @var_adress:.random_keep_value| ";

    // Save Y at .random_keep_value and subtract it from A
    asm_entry: "STY_ABS @var_adress:.random_keep_value| ";
    asm_entry: "SBC_ABS @var_adress:.random_keep_value| ";

    // Transfer the stack pointer to X, then subtract it from A
    TSX;
    asm_entry: "STX_ABS @var_adress:.random_keep_value| ";
    asm_entry: "SBC_ABS @var_adress:.random_keep_value| ";

    asm_entry: "STA_ABS @var_adress:.random_value_a| "; // Save the value of A at .random_value_a
    return .random_value_a;
}

// data for random_256 : [207, 219, 182, 74, 102, 115, 94, 22, 133, 144, 142, 137, 13, 33, 236, 109, 193, 251, 255, 96, 57, 243, 12, 136, 184, 135, 78, 162, 55, 50, 87, 20, 211, 62, 253, 140, 21, 132, 231, 92, 85, 59, 202, 75, 148, 248, 110, 128, 191, 230, 19, 30, 181, 146, 0, 100, 71, 229, 4, 139, 17, 70, 6, 152, 141, 198, 26, 45, 217, 89, 38, 46, 213, 208, 42, 107, 77, 247, 61, 129, 249, 95, 113, 197, 179, 127, 48, 214, 52, 10, 79, 130, 176, 196, 134, 86, 121, 80, 209, 157, 82, 9, 56, 175, 29, 177, 3, 63, 147, 47, 58, 14, 168, 167, 149, 54, 49, 227, 27, 7, 23, 93, 194, 44, 170, 242, 116, 15, 143, 222, 221, 166, 37, 43, 192, 216, 203, 189, 36, 215, 120, 210, 240, 226, 24, 81, 34, 98, 165, 106, 200, 64, 124, 119, 32, 187, 51, 151, 153, 164, 150, 155, 238, 72, 111, 88, 131, 195, 185, 160, 1, 5, 91, 224, 41, 173, 108, 180, 97, 68, 84, 199, 53, 126, 156, 233, 138, 73, 35, 241, 99, 169, 2, 225, 104, 172, 245, 232, 122, 206, 186, 28, 228, 145, 18, 159, 31, 69, 252, 154, 114, 246, 60, 112, 204, 103, 171, 118, 163, 244, 11, 158, 205, 117, 90, 239, 174, 101, 235, 237, 66, 218, 39, 201, 161, 178, 40, 76, 223, 183, 250, 65, 67, 254, 25, 220, 190, 234, 8, 123, 125, 188, 83, 16, 212, 105]
// Need to fix a bug on compiller (see todo)
// .random_256_pointer = 0;

// def random_256{;
//     asm_entry: "JMP_ABS @adress+259|"; // jump after the data (256 + 3)
//     asm_entry: "
//         CF DB B6 4A 66 73 5E 16 85 90 8E 89 0D 21 EC 6D C1 FB FF 60 39 F3 0C 88 B8 87 4E A2 37 32 57 14 D3 3E FD 8C 15 84 E7 5C 55 3B CA 4B 94 F8 6E 80 BF E6 13 1E B5 92 00 64 47 E5 04 8B 11 46 06 98 8D C6 1A 2D D9 59 26 2E D5 D0 2A 6B 4D F7 3D 81 F9 5F 71 C5 B3 7F 30 D6 34 0A 4F 82 B0 C4 86 56 79 50 D1 9D 52 09 38 AF 1D B1 03 3F 93 2F 3A 0E A8 A7 95 36 31 E3 1B 07 17 5D C2 2C AA F2 74 0F 8F DE DD A6 25 2B C0 D8 CB BD 24 D7 78 D2 F0 E2 18 51 22 62 A5 6A C8 40 7C 77 20 BB 33 97 99 A4 96 9B EE 48 6F 58 83 C3 B9 A0 01 05 5B E0 29 AD 6C B4 61 44 54 C7 35 7E 9C E9 8A 49 23 F1 63 A9 02 E1 68 AC F5 E8 7A CE BA 1C E4 91 12 9F 1F 45 FC 9A 72 F6 3C 70 CC 67 AB 76 A3 F4 0B 9E CD 75 5A EF AE 65 EB ED 42 DA 27 C9 A1 B2 28 4C DF B7 FA 41 43 FE 19 0D 0C BE EA 08 7B 7D BC 53 10 D4 69
//         LDX_ABS @var_adress:.random_256_pointer|
//         LDA_ABX @adress
//     ";

//     asm_entry: "STA_ABS @var_adress:.random_value_a| "; // Save the value of A at .random_value_a
//     .random_256_pointer++;
//     return .random_value_a;
// }