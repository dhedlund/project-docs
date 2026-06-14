// Beacon public messaging API. Compile from a toolkit shell:
//   cd contracts/public-api && npm install && tsp compile main.tsp
//   cp _out/openapi.yaml ../../docs/interfaces/api/openapi.yaml
import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service(#{ title: "Beacon Messaging API" })
namespace BeaconMessaging;

enum MessageStatus {
  queued,
  sent,
  delivered,
  failed,
  bounced,
}

model Message {
  id: string;
  to: string;
  channel: string;
  status: MessageStatus;

  @visibility(Lifecycle.Read)
  created: utcDateTime;
}

model SendMessage {
  to: string;

  /** email | sms | push */
  channel: string;
  template: string;

  /** Omit to send now; set to schedule for later. */
  sendAt?: utcDateTime;
}

@error
model Error {
  code: string;
  message: string;
}

@route("/messages")
namespace Messages {
  @post op send(@body body: SendMessage): Message | Error;
  @get op get(@path id: string): Message | Error;
}
