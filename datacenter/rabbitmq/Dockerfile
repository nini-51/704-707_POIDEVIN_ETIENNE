FROM rabbitmq:3

LABEL maintainer="Louis Poidevin <louis.poidevin@etudiant.univ-reims.fr>"

RUN apt-get update && apt-get install -y \
  erlang-eldap \
&& rm -rf /var/lib/apt/lists/*
RUN rabbitmq-plugins enable rabbitmq_auth_backend_ldap
