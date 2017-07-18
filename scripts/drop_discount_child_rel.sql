DROP TABLE extraschool_discount_childtype_rel;

CREATE TABLE extraschool_discount_childtype_rel
(
  extraschool_discount_version_id integer NOT NULL,
  extraschool_childtype_id integer NOT NULL,
  CONSTRAINT extraschool_discount_childtyp_extraschool_discount_version_fkey FOREIGN KEY (extraschool_discount_version_id)
      REFERENCES extraschool_discount_version (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT extraschool_discount_childtype_re_extraschool_childtype_id_fkey FOREIGN KEY (extraschool_childtype_id)
      REFERENCES extraschool_childtype (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT extraschool_discount_childtyp_extraschool_discount_version__key UNIQUE (extraschool_discount_version_id, extraschool_childtype_id)
)
WITH (
  OIDS=FALSE
);


CREATE INDEX extraschool_discount_childtype_rel_extraschool_childtype_id_ind
  ON extraschool_discount_childtype_rel
  USING btree
  (extraschool_childtype_id);


CREATE INDEX extraschool_discount_childtype_rel_extraschool_discount_version
  ON extraschool_discount_childtype_rel
  USING btree
  (extraschool_discount_version_id);