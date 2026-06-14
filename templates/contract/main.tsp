// TypeSpec contract for <service-or-api>. Compile to OpenAPI from the toolkit shell:
//   cd contracts/<name> && npm install   # once (libs resolve from local node_modules)
//   tsp compile main.tsp                  # -> _out/openapi.yaml ; copy to openapi.yaml when stable
import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service(#{ title: "<Service> API" })
namespace ServiceApi;

/** Replace this starter with the real surface (models + operations). */
model Health {
  status: string;
}

@route("/health")
@get
op health(): Health;
