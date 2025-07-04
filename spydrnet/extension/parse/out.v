//Generated from netlist by SpyDrNet
//netlist name: SDN_VERILOG_NETLIST_serial_alu
module serial_alu
(
    clk,
    reset,
    A,
    B,
    opcode,
    result,
    zero,
    carry
);

    input clk;
    input reset;
    input [3:0]A;
    input [3:0]B;
    input [1:0]opcode;
    output [3:0]result;
    output zero;
    output carry;

    wire n_59;
    wire n_58;
    wire n_57;
    wire n_56;
    wire n_55;
    wire n_54;
    wire n_53;
    wire n_52;
    wire n_51;
    wire n_50;
    wire n_49;
    wire n_48;
    wire n_47;
    wire n_46;
    wire n_45;
    wire n_44;
    wire n_43;
    wire n_42;
    wire n_41;
    wire n_40;
    wire n_39;
    wire n_38;
    wire n_37;
    wire n_36;
    wire n_35;
    wire n_34;
    wire n_33;
    wire n_32;
    wire n_31;
    wire n_30;
    wire n_29;
    wire n_28;
    wire n_27;
    wire n_26;
    wire n_25;
    wire n_24;
    wire n_23;
    wire n_22;
    wire n_21;
    wire n_20;
    wire n_19;
    wire n_18;
    wire n_17;
    wire n_16;
    wire n_15;
    wire n_14;
    wire n_13;
    wire n_12;
    wire n_11;
    wire n_10;
    wire n_9;
    wire n_8;
    wire n_7;
    wire n_6;
    wire n_5;
    wire n_4;
    wire n_3;
    wire n_2;
    wire n_1;
    wire n_0;
    wire UNCONNECTED4;
    wire UNCONNECTED3;
    wire UNCONNECTED2;
    wire UNCONNECTED1;
    wire UNCONNECTED0;
    wire UNCONNECTED;
    wire carry;
    wire zero;
    wire [3:0]result;
    wire [1:0]opcode;
    wire [3:0]B;
    wire [3:0]A;
    wire reset;
    wire clk;

    DFFRX1 zero_reg
    (
        .RN(n_58),
        .CK(clk),
        .D(n_59),
        .Q(zero),
        .QN(UNCONNECTED)
    );
    NOR4X1 g1048__2398
    (
        .A(result[1]),
        .B(result[2]),
        .C(result[0]),
        .D(result[3]),
        .Y(n_59)
    );
    DFFRX1 \result_reg[3] 
    (
        .RN(n_58),
        .CK(clk),
        .D(n_57),
        .Q(result[3]),
        .QN(UNCONNECTED0)
    );
    DFFRX1 carry_reg
    (
        .RN(n_58),
        .CK(clk),
        .D(n_56),
        .Q(carry),
        .QN(UNCONNECTED1)
    );
    OAI21X1 g1051__5107
    (
        .A0(n_52),
        .A1(n_39),
        .B0(n_54),
        .Y(n_57)
    );
    INVX1 g1053
    (
        .A(n_55),
        .Y(n_56)
    );
    DFFRX1 \result_reg[2] 
    (
        .RN(n_58),
        .CK(clk),
        .D(n_53),
        .Q(result[2]),
        .QN(UNCONNECTED2)
    );
    AOI221X1 g1054__6260
    (
        .A0(carry),
        .A1(opcode[1]),
        .B0(n_34),
        .B1(n_45),
        .C0(n_50),
        .Y(n_55)
    );
    AOI222X1 g1055__4319
    (
        .A0(n_47),
        .A1(n_41),
        .B0(opcode[1]),
        .B1(n_40),
        .C0(n_46),
        .C1(n_51),
        .Y(n_54)
    );
    OAI21X1 g1056__8428
    (
        .A0(n_52),
        .A1(n_29),
        .B0(n_48),
        .Y(n_53)
    );
    DFFRX1 \result_reg[1] 
    (
        .RN(n_58),
        .CK(clk),
        .D(n_44),
        .Q(result[1]),
        .QN(UNCONNECTED3)
    );
    CLKXOR2X1 g1058__5526
    (
        .A(n_49),
        .B(n_38),
        .Y(n_51)
    );
    AOI211X1 g1059__6783
    (
        .A0(n_11),
        .A1(n_49),
        .B0(n_16),
        .C0(n_43),
        .Y(n_50)
    );
    AOI222X1 g1057__3680
    (
        .A0(n_47),
        .A1(n_23),
        .B0(opcode[1]),
        .B1(n_21),
        .C0(n_46),
        .C1(n_36),
        .Y(n_48)
    );
    INVX1 g1061
    (
        .A(n_42),
        .Y(n_45)
    );
    OAI21X1 g1063__1617
    (
        .A0(n_43),
        .A1(n_30),
        .B0(n_35),
        .Y(n_44)
    );
    AOI21X1 g1062__2802
    (
        .A0(n_41),
        .A1(n_37),
        .B0(n_40),
        .Y(n_42)
    );
    CLKXOR2X1 g1065__1705
    (
        .A(n_38),
        .B(n_37),
        .Y(n_39)
    );
    OAI21X1 g1066__5122
    (
        .A0(n_15),
        .A1(n_33),
        .B0(n_14),
        .Y(n_49)
    );
    CLKXOR2X1 g1064__8246
    (
        .A(n_32),
        .B(n_28),
        .Y(n_36)
    );
    AOI222X1 g1068__7098
    (
        .A0(n_47),
        .A1(n_17),
        .B0(opcode[1]),
        .B1(n_5),
        .C0(n_34),
        .C1(n_27),
        .Y(n_35)
    );
    DFFRX1 \result_reg[0] 
    (
        .RN(n_58),
        .CK(clk),
        .D(n_31),
        .Q(result[0]),
        .QN(UNCONNECTED4)
    );
    INVX1 g1069
    (
        .A(n_24),
        .Y(n_37)
    );
    INVX1 g1070
    (
        .A(n_32),
        .Y(n_33)
    );
    OAI221X1 g1073__6131
    (
        .A0(opcode[1]),
        .A1(n_19),
        .B0(n_1),
        .B1(n_26),
        .C0(n_12),
        .Y(n_31)
    );
    CLKXOR2X1 g1074__1881
    (
        .A(n_20),
        .B(n_25),
        .Y(n_30)
    );
    CLKXOR2X1 g1075__5115
    (
        .A(n_28),
        .B(n_22),
        .Y(n_29)
    );
    CLKXOR2X1 g1076__7482
    (
        .A(n_26),
        .B(n_25),
        .Y(n_27)
    );
    AOI21X1 g1071__4733
    (
        .A0(n_23),
        .A1(n_22),
        .B0(n_21),
        .Y(n_24)
    );
    OAI22X1 g1072__6161
    (
        .A0(n_9),
        .A1(n_20),
        .B0(B[1]),
        .B1(n_8),
        .Y(n_32)
    );
    ADDHX1 g1077__9315
    (
        .A(B[0]),
        .B(n_0),
        .CO(n_20),
        .S(n_19)
    );
    OAI21X1 g1078__9945
    (
        .A0(n_26),
        .A1(n_2),
        .B0(n_18),
        .Y(n_22)
    );
    NAND2X1 g1079__2883
    (
        .A(n_18),
        .B(n_17),
        .Y(n_25)
    );
    NOR2X1 g1080__2346
    (
        .A(n_10),
        .B(n_16),
        .Y(n_38)
    );
    NOR2X1 g1082__1666
    (
        .A(n_15),
        .B(n_13),
        .Y(n_28)
    );
    INVX1 g1083
    (
        .A(n_13),
        .Y(n_14)
    );
    OAI21X1 g1081__7410
    (
        .A0(B[0]),
        .A1(A[0]),
        .B0(n_47),
        .Y(n_12)
    );
    INVX1 g1084
    (
        .A(n_10),
        .Y(n_11)
    );
    CLKINVX2 g1085
    (
        .A(n_43),
        .Y(n_46)
    );
    AND2X1 g1086__6417
    (
        .A(n_8),
        .B(B[1]),
        .Y(n_9)
    );
    INVX1 g1095
    (
        .A(n_34),
        .Y(n_52)
    );
    NOR2X1 g1087__5477
    (
        .A(B[3]),
        .B(n_4),
        .Y(n_16)
    );
    NOR2X1 g1088__2398
    (
        .A(B[2]),
        .B(n_7),
        .Y(n_13)
    );
    NAND2X1 g1097__5107
    (
        .A(n_7),
        .B(n_6),
        .Y(n_23)
    );
    NOR2X1 g1089__6260
    (
        .A(A[2]),
        .B(n_6),
        .Y(n_15)
    );
    INVX1 g1094
    (
        .A(n_18),
        .Y(n_5)
    );
    NAND2X1 g1098__4319
    (
        .A(n_4),
        .B(n_3),
        .Y(n_41)
    );
    NOR2X1 g1096__8428
    (
        .A(n_4),
        .B(n_3),
        .Y(n_40)
    );
    INVX1 g1093
    (
        .A(n_2),
        .Y(n_17)
    );
    NOR2X1 g1090__5526
    (
        .A(A[3]),
        .B(n_3),
        .Y(n_10)
    );
    NAND2X1 g1092__6783
    (
        .A(opcode[0]),
        .B(n_1),
        .Y(n_43)
    );
    NAND2X1 g1103__3680
    (
        .A(B[0]),
        .B(A[0]),
        .Y(n_26)
    );
    NOR2X1 g1101__1617
    (
        .A(opcode[0]),
        .B(opcode[1]),
        .Y(n_34)
    );
    AND2X1 g1102__2802
    (
        .A(opcode[1]),
        .B(opcode[0]),
        .Y(n_47)
    );
    NOR2X1 g1099__1705
    (
        .A(B[1]),
        .B(A[1]),
        .Y(n_2)
    );
    AND2X1 g1091__5122
    (
        .A(A[2]),
        .B(B[2]),
        .Y(n_21)
    );
    NAND2X1 g1100__8246
    (
        .A(B[1]),
        .B(A[1]),
        .Y(n_18)
    );
    CLKINVX2 g1110
    (
        .A(A[0]),
        .Y(n_0)
    );
    CLKINVX2 g1107
    (
        .A(A[2]),
        .Y(n_7)
    );
    CLKINVX2 g1105
    (
        .A(A[1]),
        .Y(n_8)
    );
    INVX2 g1108
    (
        .A(B[3]),
        .Y(n_3)
    );
    CLKINVX2 g1106
    (
        .A(opcode[1]),
        .Y(n_1)
    );
    INVX2 g1104
    (
        .A(B[2]),
        .Y(n_6)
    );
    INVX2 g1109
    (
        .A(A[3]),
        .Y(n_4)
    );
    INVX1 g1111
    (
        .A(reset),
        .Y(n_58)
    );
endmodule

`celldefine
module DFFRX1
(
    RN,
    CK,
    D,
    Q,
    QN
);

    /* undefined port direction */ inout RN;
    /* undefined port direction */ inout CK;
    /* undefined port direction */ inout D;
    /* undefined port direction */ inout Q;
    /* undefined port direction */ inout QN;

endmodule
`endcelldefine

`celldefine
module NOR4X1
(
    A,
    B,
    C,
    D,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout B;
    /* undefined port direction */ inout C;
    /* undefined port direction */ inout D;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module OAI21X1
(
    A0,
    A1,
    B0,
    Y
);

    /* undefined port direction */ inout A0;
    /* undefined port direction */ inout A1;
    /* undefined port direction */ inout B0;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module INVX1
(
    A,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module AOI221X1
(
    A0,
    A1,
    B0,
    B1,
    C0,
    Y
);

    /* undefined port direction */ inout A0;
    /* undefined port direction */ inout A1;
    /* undefined port direction */ inout B0;
    /* undefined port direction */ inout B1;
    /* undefined port direction */ inout C0;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module AOI222X1
(
    A0,
    A1,
    B0,
    B1,
    C0,
    C1,
    Y
);

    /* undefined port direction */ inout A0;
    /* undefined port direction */ inout A1;
    /* undefined port direction */ inout B0;
    /* undefined port direction */ inout B1;
    /* undefined port direction */ inout C0;
    /* undefined port direction */ inout C1;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module CLKXOR2X1
(
    A,
    B,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout B;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module AOI211X1
(
    A0,
    A1,
    B0,
    C0,
    Y
);

    /* undefined port direction */ inout A0;
    /* undefined port direction */ inout A1;
    /* undefined port direction */ inout B0;
    /* undefined port direction */ inout C0;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module AOI21X1
(
    A0,
    A1,
    B0,
    Y
);

    /* undefined port direction */ inout A0;
    /* undefined port direction */ inout A1;
    /* undefined port direction */ inout B0;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module OAI221X1
(
    A0,
    A1,
    B0,
    B1,
    C0,
    Y
);

    /* undefined port direction */ inout A0;
    /* undefined port direction */ inout A1;
    /* undefined port direction */ inout B0;
    /* undefined port direction */ inout B1;
    /* undefined port direction */ inout C0;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module OAI22X1
(
    A0,
    A1,
    B0,
    B1,
    Y
);

    /* undefined port direction */ inout A0;
    /* undefined port direction */ inout A1;
    /* undefined port direction */ inout B0;
    /* undefined port direction */ inout B1;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module ADDHX1
(
    A,
    B,
    CO,
    S
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout B;
    /* undefined port direction */ inout CO;
    /* undefined port direction */ inout S;

endmodule
`endcelldefine

`celldefine
module NAND2X1
(
    A,
    B,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout B;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module NOR2X1
(
    A,
    B,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout B;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module CLKINVX2
(
    A,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module AND2X1
(
    A,
    B,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout B;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

`celldefine
module INVX2
(
    A,
    Y
);

    /* undefined port direction */ inout A;
    /* undefined port direction */ inout Y;

endmodule
`endcelldefine

