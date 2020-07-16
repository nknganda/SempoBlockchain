import React from "react";
import { Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";

//todo: deprecate mainSpinner, miniSpinner
export default class LoadingSpinner extends React.Component {
  render() {
    let icon = (
      <LoadingOutlined style={{ fontSize: 24 }} spin {...this.props} />
    );
    return <Spin indicator={icon} />;
  }
}
