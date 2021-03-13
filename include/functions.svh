`ifndef _OPENHDL_FUNCTIONS_SVH_
`define _OPENHDL_FUNCTIONS_SVH_

function integer clog2;
  input integer value;
  begin
    value = value - 1;
    for (clog2 = 0; value > 0; clog2 = clog2 + 1) value = value >> 1;
  end
endfunction

`endif // _OPENHDL_FUNCTIONS_SVH_