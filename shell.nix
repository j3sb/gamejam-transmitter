let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      matplotlib numpy pyserial scipy
    ]))
    pkgs.gcc-arm-embedded
    pkgs.cmake
    pkgs.picotool
  ];
  PICO_SDK_PATH="${pkgs.pico-sdk.override { withSubmodules = true; }}/lib/pico-sdk";
}
