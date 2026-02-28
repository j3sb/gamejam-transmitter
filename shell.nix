let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
      matplotlib numpy pyserial scipy
    ]))
    pkgs.gcc-arm-embedded
  ];
}

