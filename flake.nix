{
  description = "5G Core deploy devshell with Ansible";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python packages
            python312
            python312Packages.pip
            python312Packages.setuptools
            python312Packages.wheel

            # Build tools
            ninja
            flex
            bison
            meson
            pkg-config

            # Libraries
            lksctp-tools # libsctp-dev
            gnutls # libgnutls28-dev
            libgcrypt # libgcrypt-dev
            openssl # libssl-dev
            libyaml # libyaml-dev
            nghttp2 # libnghttp2-dev
            libmicrohttpd # libmicrohttpd-dev
            libtins # libtins-dev
            talloc # libtalloc-dev
            mongoc # libmongoc-1.0, libbson
            libidn # libidn-dev
            curl # libcurl-dev
          ];

          shellHook = ''
          '';
        };
      }
    );
}
