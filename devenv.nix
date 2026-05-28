{ pkgs, lib, ... }:

let
  # Cross-compilation pkgs using the standard pkgsCross provided by devenv's nixpkgs
  crossPkgs = pkgs.pkgsCross.aarch64-multiplatform;

  # System libraries needed for CEF/Graphics
  cefLibs = with pkgs; [
    wayland libxkbcommon mesa libGL libglvnd glib vulkan-loader
    nss nspr atk dbus cups libdrm libgbm libxshmfence udev
    expat cairo pango systemd alsa-lib pciutils
    libX11 libXcomposite libXdamage libXext
    libXfixes libXrandr libXrender libxtst libxcb
  ];
in
{
  # 1. RUST TOOLCHAIN
  languages.rust = {
    enable = true;
    components = [ "rustc" "cargo" "rust-analyzer" "rustfmt" "clippy" ];
  };

  # 2. CROSS-COMPILATION PROFILE
  profiles.aarch64.module = {
    languages.rust.targets = [ "aarch64-unknown-linux-gnu" ];

    env = {
      CARGO_BUILD_TARGET = "aarch64-unknown-linux-gnu";
      CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER =
        "${crossPkgs.stdenv.cc}/bin/${crossPkgs.stdenv.cc.targetPrefix}cc";
      PKG_CONFIG_ALLOW_CROSS = "1";
    };

    packages = [ crossPkgs.pkg-config ];
  };

  # 3. CEF SYSTEM ENVIRONMENT
  packages = with pkgs; [
    pkg-config
    openssl
    fontconfig
    freetype
  ] ++ cefLibs;

  env = {
    # Automatically build the LD_LIBRARY_PATH from the list above
    LD_LIBRARY_PATH = lib.makeLibraryPath cefLibs;
  };

  # 4. AUTOMATION (The CEF Symlink Logic)
  enterShell = ''
    # Determine the target directory based on current profile/system
    if [ "$CARGO_BUILD_TARGET" = "aarch64-unknown-linux-gnu" ]; then
        target_base="rustclock/target/aarch64-unknown-linux-gnu"
    else
        target_base="rustclock/target"
    fi

    for profile in debug release; do
      target_dir="$target_base/$profile"
      if [ -d "$target_dir" ]; then
        # Find CEF directory and symlink contents
        cef_dir=$(find rustclock/target -type d -name "cef_linux_*" | head -n 1)
        if [ -n "$cef_dir" ]; then
          ln -sf "$PWD/$cef_dir"/* "$target_dir/" 2>/dev/null || true
        fi
      fi
    done

    # Update LD_LIBRARY_PATH to include local build artifacts
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$PWD/rustclock/target/debug:$PWD/rustclock/target/release"

    echo -e "\U0001f980 Rust + CEF environment active"
    [ -n "$CARGO_BUILD_TARGET" ] && echo -e "\U0001f3af Target: $CARGO_BUILD_TARGET"
  '';
}
