let
  nixconfig = builtins.getFlake "github:death916/nixconfig";
  unstable = nixconfig.inputs.nixpkgs-unstable.legacyPackages.x86_64-linux;
  pkgs = nixconfig.inputs.nixpkgs.legacyPackages.x86_64-linux;
in
pkgs.mkShell {
  packages = with pkgs; [
    python313Packages.uv
    python313Packages.ninja
    python313Packages.numpy
    bun
    unstable.rustc
    unstable.cargo
    unstable.rust-analyzer
    unstable.rustfmt
    pkgs.pkg-config
    pkgs.openssl
    pkgs.libxcb
    pkgs.pkg-config
    pkgs.openssl
    pkgs.alsa-lib
    pkgs.libxcb
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.fontconfig
    pkgs.freetype
    pkgs.mesa
    pkgs.libGL
    pkgs.glib
    pkgs.vulkan-loader
    pkgs.vulkan-headers
    pkgs.clippy
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.mesa
    pkgs.glib
    pkgs.vulkan-loader
  ];

  shellHook = ''
    source .venv/bin/activate
    # export PATH="${pkgs.bun}/bin:$PATH"
    # export BUN_INSTALL="${pkgs.bun}/bin/bun"
    export REFLEX_USE_SYSTEM_BUN=True
    echo venv activated and bun versions set
  '';
}
