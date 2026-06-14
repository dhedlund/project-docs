// Beacon billing-service — HTTP contract (TypeSpec authoring layer).
// Compile to OpenAPI:  npx @typespec/compiler compile main.tsp --emit @typespec/openapi3
import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service(#{ title: "Beacon Billing" })
namespace BeaconBilling;

/** Lifecycle status. Note: in the real service this is enforced in app code,
 *  not the database — the contract just documents the allowed values. */
enum SubscriptionStatus {
  trialing,
  active,
  past_due,
  canceled,
}

model Subscription {
  id: string;
  orgId: string;
  planId: string;
  status: SubscriptionStatus;
  seats: int32;

  /** Derived from a DB view (active_subscriptions_v); read-only. */
  @visibility(Lifecycle.Read)
  seatsInUse: int32;

  currentPeriodEnd: utcDateTime;
}

model UpgradeRequest {
  planId: string;
}

@error
model Error {
  code: string;
  message: string;
}

@route("/subscriptions")
namespace Subscriptions {
  @get op get(@path id: string): Subscription | Error;

  @route("/{id}/upgrade")
  @post
  op upgrade(@path id: string, @body body: UpgradeRequest): Subscription | Error;
}
